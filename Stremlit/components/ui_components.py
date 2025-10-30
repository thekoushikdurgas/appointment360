"""
Reusable UI Components with Modern Styling
"""
import streamlit as st
from utils.theme_manager import ThemeManager


def styled_metric_card(label: str, value, delta=None, icon="📊"):
    """Display a styled metric card"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{icon}</div>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.metric(label=label, value=value, delta=delta)
    
    st.markdown("<br>", unsafe_allow_html=True)


def icon_button(label: str, icon: str = "🔘", button_type: str = "primary", key=None):
    """Create a button with icon"""
    return st.button(f"{icon} {label}", type=button_type, key=key)


def styled_card(title: str = "", content=None):
    """Create a styled card container"""
    st.markdown(f"""
    <div class="element-container">
        <h3 style='color: var(--primary-color); margin-bottom: 1rem;'>{title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if content:
        st.markdown(content, unsafe_allow_html=True)


def badge(status: str, variant: str = "success"):
    """Display a status badge"""
    colors = {
        "success": "🟢",
        "error": "🔴",
        "warning": "🟡",
        "info": "🔵"
    }
    return colors.get(variant, "⚪")


def notification_box(message: str, type: str = "info"):
    """Display a styled notification"""
    icons = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    
    if type == "success":
        st.success(f"{icons.get(type, '')} {message}")
    elif type == "error":
        st.error(f"{icons.get(type, '')} {message}")
    elif type == "warning":
        st.warning(f"{icons.get(type, '')} {message}")
    else:
        st.info(f"{icons.get(type, '')} {message}")


def progress_bar_with_text(current: float, total: float, label: str = ""):
    """Display a progress bar with percentage text"""
    percentage = (current / total * 100) if total > 0 else 0
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(percentage / 100)
    with col2:
        st.markdown(f"**{percentage:.1f}%**")
    
    if label:
        st.caption(f"{label}: {current:,} / {total:,}")


def divider():
    """Add a styled divider"""
    colors = ThemeManager.get_colors()
    st.markdown(f"""
    <div style="height: 1px; background: linear-gradient(90deg, 
    transparent, {colors['borderColor']}, transparent); margin: 1rem 0;"></div>
    """, unsafe_allow_html=True)


def hero_section(title: str, subtitle: str, icon: str = "🌟"):
    """Display a hero section with gradient background"""
    colors = ThemeManager.get_colors()
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {colors['primaryColor']}22, {colors['primaryColor']}11);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid {colors['borderColor']};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="color: {colors['textColor']}; margin-bottom: 0.5rem;">
            {icon} {title}
        </h1>
        <p style="color: {colors['textColor']}AA; font-size: 1.1rem; margin: 0;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, value: str, icon: str = "📌"):
    """Display an info card"""
    colors = ThemeManager.get_colors()
    
    return st.markdown(f"""
    <div style="
        background: {colors['secondaryBackgroundColor']};
        border-left: 4px solid {colors['primaryColor']};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    ">
        <strong>{icon} {title}:</strong> {value}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, icon: str = ""):
    """Display a styled section header"""
    colors = ThemeManager.get_colors()
    
    st.markdown(f"""
    <h2 style="
        color: {colors['primaryColor']};
        border-bottom: 2px solid {colors['primaryColor']};
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    ">
        {icon} {title}
    </h2>
    """, unsafe_allow_html=True)

