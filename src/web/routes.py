from flask import Blueprint, jsonify, request, render_template, send_file, session
from ..correlation.correlation_engine import CorrelationEngine
from ..generator.explanation_generator import ExplanationGenerator
from ..feedback.user_feedback import user_feedback
from .translations import get_translation, get_supported_languages, get_language_names, TRANSLATIONS
from functools import wraps
import time
from datetime import datetime, timedelta
import threading
import logging
import traceback
from io import BytesIO
import plotly.io as pio
import numpy as np
import plotly.graph_objects as go
from scipy import stats

# Configuration du logging
logger = logging.getLogger(__name__)

bp = Blueprint('web', __name__)
correlation_engine = CorrelationEngine()
explanation_generator = ExplanationGenerator()

# Rate limiting configuration
RATE_LIMIT = {
    'window_size': 60,  # in seconds
    'max_requests': 30  # maximum number of requests per window
}

# Dictionary to store requests
request_counts = {}
request_lock = threading.Lock()

# Simple cache to store correlations
correlation_cache = {}

def store_correlation(correlation):
    """Store a correlation in cache."""
    correlation_id = correlation.get('correlation_id', f'corr_{int(time.time())}')
    correlation_cache[correlation_id] = correlation
    return correlation_id

def get_correlation(correlation_id):
    """Retrieve a correlation from cache."""
    return correlation_cache.get(correlation_id)

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        with request_lock:
            # Clean old entries
            request_counts.clear()
            
            # Check and update counter
            if client_ip in request_counts:
                requests = request_counts[client_ip]
                # Remove requests older than window
                requests = [req for req in requests if current_time - req < RATE_LIMIT['window_size']]
                
                if len(requests) >= RATE_LIMIT['max_requests']:
                    return jsonify({
                        'status': 'error',
                        'message': 'Too many requests. Please try again in a few minutes.',
                        'retry_after': int(RATE_LIMIT['window_size'] - (current_time - requests[0]))
                    }), 429
                
                requests.append(current_time)
                request_counts[client_ip] = requests
            else:
                request_counts[client_ip] = [current_time]
        
        return f(*args, **kwargs)
    return decorated_function

def get_user_language():
    """Récupère la langue de l'utilisateur depuis la session ou la requête."""
    # 1. Vérifier si une langue est spécifiée dans l'URL
    lang = request.args.get('lang')
    if lang and lang in get_supported_languages():
        session['language'] = lang
        session.permanent = True  # Make session persistent
        logger.debug(f"Language set from URL: {lang}")
        return lang
    
    # 2. Vérifier la session
    if 'language' in session and session['language'] in get_supported_languages():
        logger.debug(f"Language from session: {session['language']}")
        return session['language']
    
    # 3. Vérifier l'en-tête Accept-Language du navigateur
    browser_lang = request.headers.get('Accept-Language', '')
    if 'fr' in browser_lang.lower():
        session['language'] = 'fr'
        session.permanent = True
        logger.debug(f"Language detected from browser: fr")
        return 'fr'
    
    # 4. Par défaut: anglais
    session['language'] = 'en'
    session.permanent = True
    logger.debug(f"Language defaulted to: en")
    return 'en'

@bp.route('/')
def index():
    lang = get_user_language()
    translations = TRANSLATIONS[lang]
    return render_template('index.html', lang=lang, t=translations, language_names=get_language_names())

@bp.route('/set_language/<lang>')
def set_language(lang):
    """Définit la langue de l'utilisateur."""
    if lang in get_supported_languages():
        session['language'] = lang
    return jsonify({'status': 'success', 'language': session.get('language', 'en')})

@bp.route('/favicon.ico')
def favicon():
    """Serve Chartastrophe ICO favicon."""
    from flask import send_from_directory
    import os
    return send_from_directory(
        os.path.join(bp.root_path, 'static'), 
        'favicon.ico', 
        mimetype='image/x-icon'
    )

@bp.route('/favicon.svg')
def favicon_svg():
    """Serve modern Chartastrophe SVG favicon."""
    from flask import send_from_directory
    import os
    return send_from_directory(
        os.path.join(bp.root_path, 'static'), 
        'favicon.svg', 
        mimetype='image/svg+xml'
    )

@bp.route('/api/correlation/random')
@rate_limit
def get_random_correlation():
    try:
        logger.info("Random correlation request received")
        
        # Check feedback stats to inform user
        feedback_stats = user_feedback.get_stats()
        if feedback_stats['total_feedback'] > 0:
            logger.info(f"Feedback influence: {feedback_stats['total_feedback']} evaluations, "
                       f"{feedback_stats['funny_ratio']:.1%} funny, top dataset: {feedback_stats['top_funny_datasets'][0][0] if feedback_stats['top_funny_datasets'] else 'none'}")
        
        # Get user language for dataset generation
        user_lang = get_user_language()
        logger.info(f"🌐 Generating datasets with language: {user_lang}")
        
        # Generate correlation
        correlations = correlation_engine.generate_random_correlations(n_datasets=8, lang=user_lang)
        
        if not correlations:
            logger.warning("No correlation generated")
            return jsonify({
                'status': 'error',
                'message': 'Unable to generate an interesting correlation at the moment. Please try again in a few moments.'
            }), 500
        
        # Take the first correlation
        correlation = correlations[0]
        
        logger.debug("Generating explanation...")
        # Always regenerate explanation with correct language (overwrite engine's default)
        try:
            # Get user language for explanation generation
            user_lang = get_user_language()
            logger.info(f"🌐 Detected user language: {user_lang}")
            logger.info(f"📝 Session language: {session.get('language', 'NOT_SET')}")
            logger.info(f"🔍 URL lang param: {request.args.get('lang', 'NOT_SET')}")
            explanation = explanation_generator.generate_explanation(correlation, language=user_lang)
            logger.info(f"✅ Generated explanation title: {explanation.get('title', 'NO_TITLE')[:50]}...")
            correlation['explanation'] = explanation
        except Exception as ex_e:
            logger.warning(f"Error generating explanation: {str(ex_e)}")
            user_lang = get_user_language()
            if user_lang == 'fr':
                correlation['explanation'] = {
                    'title': "📊 Analyse statistique en cours",
                    'explanation': "Une corrélation intéressante a été détectée par nos algorithmes d'analyse. L'équipe de recherche étudie actuellement les implications de cette découverte dans un cadre méthodologique rigoureux."
                }
            else:
                correlation['explanation'] = {
                    'title': "📊 Statistical analysis in progress", 
                    'explanation': "An interesting correlation has been detected by our analysis algorithms. The research team is currently studying the implications of this discovery within a rigorous methodological framework."
                }
        
        logger.debug("Explanation generated successfully")
        
        # Store correlation in cache
        correlation_id = store_correlation(correlation)
        correlation['correlation_id'] = correlation_id
        
        logger.info(f"Correlation generated successfully: {correlation['series1_name']} vs {correlation['series2_name']} (r={correlation.get('correlation', correlation.get('correlation_coefficient', 0)):.3f})")
        
        return jsonify({
            'status': 'success',
            'data': correlation
        })
    except Exception as e:
        logger.error(f"Error generating correlation: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred while generating the correlation.'
        }), 500

@bp.route('/api/correlation/graph/<correlation_id>')
@rate_limit
def get_correlation_graph(correlation_id):
    try:
        logger.debug(f"Retrieving graph for correlation {correlation_id}")
        correlation = get_correlation(correlation_id)
        
        if correlation is None:
            logger.warning(f"Correlation {correlation_id} not found")
            return jsonify({
                'status': 'error',
                'message': 'Correlation not found'
            }), 404
            
        logger.debug("Generating graph data")
        plot_data = generate_plot_data(correlation)
        logger.debug("Graph data generated successfully")
        
        return jsonify({
            'status': 'success',
            'data': plot_data
        })
    except Exception as e:
        logger.error(f"Error generating graph: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while generating the graph.'
        }), 500

def generate_plot_data(correlation):
    """Generate data for chart with correlation line."""
    data_x = correlation.get('data_x', [])
    data_y = correlation.get('data_y', [])
    series1_name = correlation.get('series1_name', 'Variable 1')
    series2_name = correlation.get('series2_name', 'Variable 2')
    coef = correlation.get('correlation_coefficient', correlation.get('correlation', 0))
    sources = correlation.get('sources', [])
    
    # Create scatter plot with colors by source
    fig = go.Figure()
    
    # Color palette for sources
    source_colors = [
        'rgba(55, 126, 184, 0.8)',   # Blue for series 1
        'rgba(228, 26, 28, 0.8)',   # Red for series 2
        'rgba(77, 175, 74, 0.8)',   # Green (just in case)
        'rgba(152, 78, 163, 0.8)',  # Purple (just in case)
    ]
    
    # Determine the color of each point based on its origin
    # Each point comes from either data_x (series 1) or data_y (series 2)
    # For simplicity, we can alternate or use the dataset index
    
            # Retrieve dataset indices if available
    dataset1_index = correlation.get('dataset1_index', 0)
    dataset2_index = correlation.get('dataset2_index', 1)
    
    # Unique color for all points
    point_color = 'rgba(55, 126, 184, 0.7)'  # Uniform blue
    
            # Add points with unique color
    fig.add_trace(go.Scatter(
        x=data_x,
        y=data_y,
        mode='markers',
        name='Observed data',
        marker=dict(
            size=6,  # Standard size
            color=point_color,
            line=dict(width=1, color='white'),
            symbol='circle'
        ),
        hovertemplate=f'<b>{series1_name}</b>: %{{x:.2f}}<br><b>{series2_name}</b>: %{{y:.2f}}<br><i>Point n°%{{pointNumber}}</i><extra></extra>'
    ))
    
            # Calculate and add regression line with statistics
    if len(data_x) > 1 and len(data_y) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(data_x, data_y)
        x_line = [min(data_x), max(data_x)]
        y_line = [slope * x + intercept for x in x_line]
        
        # Confidence zone (approximate) more subtle
        x_range = max(data_x) - min(data_x)
        y_upper = [y + std_err * x_range * 0.05 for y in y_line]  # Smaller zone
        y_lower = [y - std_err * x_range * 0.05 for y in y_line]
        
        # Add the confidence zone
        fig.add_trace(go.Scatter(
            x=x_line + x_line[::-1],
            y=y_upper + y_lower[::-1],
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.05)',  # Even more transparent
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            hoverinfo='skip',
            name='Confidence zone'
        ))
        
        # Add regression line in dashed style
        fig.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name=f'Linear regression (r={coef:.3f})',
            line=dict(color='red', width=1, dash='dash'),  # Dashed line
            hovertemplate=f'<b>Regression line</b><br>y = {slope:.2f}x + {intercept:.2f}<br>r = {coef:.3f}<br>p-value = {p_value:.3e}<extra></extra>'
        ))
    
    # Calculate descriptive statistics for annotations
    n_points = len(data_x)
    mean_x = sum(data_x) / len(data_x) if data_x else 0
    mean_y = sum(data_y) / len(data_y) if data_y else 0
    
    # Format graph with more information
    fig.update_layout(
        title=dict(
            text=f'<b>Correlation Analysis</b><br><i>{series1_name} vs {series2_name}</i><br><span style="font-size:12px">n = {n_points} observations • r = {coef:.3f}</span>',
            x=0.5,
            font=dict(size=16, color='#2c3e50'),
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text=f'<b>{series1_name}</b><br><i>Moyenne: {mean_x:.2f}</i>',
                font=dict(size=14)
            ),
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor='#333',
            mirror=True
        ),
        yaxis=dict(
            title=dict(
                text=f'<b>{series2_name}</b><br><i>Moyenne: {mean_y:.2f}</i>',
                font=dict(size=14)
            ),
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor='#333',
            mirror=True
        ),
        font=dict(size=12, family="Arial, sans-serif"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.3)",
            borderwidth=1,
            font=dict(size=11)
        ),
        margin=dict(l=80, r=40, t=100, b=80),
        hovermode='closest'
    )
    
    # Add annotation with statistics
    correlation_strength = "strong" if abs(coef) > 0.7 else "moderate" if abs(coef) > 0.4 else "weak"
    direction = "positive" if coef > 0 else "negative"
    
    fig.add_annotation(
        x=0.02,
        y=0.02,
        xref="paper",
        yref="paper",
        text=f"<b>{correlation_strength} {direction} correlation</b><br>{n_points} points analyzed",
        showarrow=False,
        font=dict(size=10, color="#666"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=1
    )
    
    return fig.to_json()

@bp.route('/share/<correlation_id>')
def share_correlation(correlation_id):
    try:
        lang = get_user_language()
        translations = TRANSLATIONS[lang]
        correlation = get_correlation(correlation_id)
        
        if correlation is None:
            return render_template('error.html', 
                message=get_translation(lang, 'error_not_found'),
                lang=lang, 
                t=translations, 
                language_names=get_language_names()), 404
        
        return render_template('share.html', 
                             correlation=correlation,
                             lang=lang, 
                             t=translations, 
                             language_names=get_language_names())
    except Exception as e:
        logging.error(f"Error displaying shared correlation: {str(e)}")
        lang = get_user_language()
        translations = TRANSLATIONS[lang]
        return render_template('error.html', 
            message=get_translation(lang, 'error_unexpected'),
            lang=lang, 
            t=translations, 
            language_names=get_language_names()), 500

@bp.route('/api/correlation/share-image/<correlation_id>')
def generate_share_image(correlation_id):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return jsonify({'status': 'error', 'message': 'PIL (Pillow) is not installed'}), 500
    
    correlation = get_correlation(correlation_id)
    if not correlation:
        return jsonify({'status': 'error', 'message': 'Correlation not found'}), 404
    
    # Generate the graph in image format
    fig = correlation.get_plot_figure() if hasattr(correlation, 'get_plot_figure') else None
    if fig is None:
        return jsonify({'status': 'error', 'message': 'Unable to generate graph'}), 500
    plot_img = Image.open(BytesIO(pio.to_image(fig, format='png')))
    
    # Create larger image to contain graph and text
    width = 1200
    height = 1000  # Increased to accommodate sources
    image = Image.new('RGB', (width, height), 'white')
    
    # Add the title
    draw = ImageDraw.Draw(image)
    try:
        # First try common system fonts
        font_paths = [
            'arial.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            'C:\\Windows\\Fonts\\arial.ttf'
        ]
        
        font_title = None
        for font_path in font_paths:
            try:
                font_title = ImageFont.truetype(font_path, 36)
                font_text = ImageFont.truetype(font_path, 24)
                font_small = ImageFont.truetype(font_path, 18)
                break
            except (OSError, IOError):
                continue
        
        if font_title is None:
            raise OSError("No system fonts found")
            
    except Exception as e:
        logger.warning(f"Unable to load system fonts: {str(e)}. Using default fonts.")
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add the logo and title
    draw.text((50, 50), "Correlactions", fill='black', font=font_title)
    draw.text((50, 100), getattr(correlation, 'title', ''), fill='black', font=font_text)
    
    # Add the explanation
    explanation = getattr(correlation, 'explanation', '')
    explanation_lines = wrap_text(explanation, font_text, width - 100)
    y = 150
    for line in explanation_lines:
        draw.text((50, y), line, fill='black', font=font_text)
        y += 30
    
    # Add the graph
    plot_img = plot_img.resize((width - 100, 400), Image.LANCZOS)
    image.paste(plot_img, (50, 300))
    
    # Add the statistics
    coef = getattr(correlation, 'correlation_coefficient', getattr(correlation, 'coefficient', 0))
    stats_text = f"Correlation coefficient: {coef:.1%}"
    draw.text((50, height - 250), stats_text, fill='black', font=font_text)
    
    # Add sources
    source1 = getattr(correlation, 'series1_name', getattr(correlation, 'source_name_1', ''))
    source2 = getattr(correlation, 'series2_name', getattr(correlation, 'source_name_2', ''))
    draw.text((50, height - 200), "Data sources:", fill='black', font=font_text)
    draw.text((50, height - 160), f"Variable 1 : {source1}", fill='black', font=font_small)
    draw.text((50, height - 130), f"Variable 2 : {source2}", fill='black', font=font_small)
    
    # Add the link to the site
    draw.text((50, height - 50), "Discover more at correlactions.fr", fill='black', font=font_text)
    
    # Save the image in memory
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

def wrap_text(text, font, max_width):
    """Utility function to wrap text"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if hasattr(font, 'getlength'):
            length = font.getlength(test_line)
        else:
            length = font.getsize(test_line)[0]
        if length <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

@bp.route('/api/feedback', methods=['POST'])
@rate_limit
def submit_feedback():
    try:
        data = request.get_json()
        correlation_id = data.get('correlation_id')
        rating = data.get('rating')  # 'funny' ou 'boring'
        series1_name = data.get('series1_name')
        series2_name = data.get('series2_name')
        
        if not all([correlation_id, rating, series1_name, series2_name]):
            return jsonify({
                'status': 'error',
                'message': 'Missing data'
            }), 400
            
        if rating not in ['funny', 'intriguing', 'boring']:
            return jsonify({
                'status': 'error',
                'message': 'Invalid rating'
            }), 400
        
        # Add the feedback
        user_feedback.add_feedback(correlation_id, rating, series1_name, series2_name)
        
        logger.info(f"Feedback received: {rating} for {correlation_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback recorded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error saving feedback'
        }), 500

@bp.route('/api/feedback/stats')
def get_feedback_stats():
    try:
        stats = user_feedback.get_stats()
        return jsonify({
            'status': 'success',
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error retrieving statistics'
        }), 500 