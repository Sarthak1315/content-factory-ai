
"""
Content Factory AI - Complete Web UI with Brand Voice Management
"""

import streamlit as st
import asyncio
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import time
import plotly.graph_objects as go
import plotly.express as px

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

st.set_page_config(
    page_title="Content Factory AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)


class StreamlitContentFactory:
    """Streamlit wrapper for Content Factory"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.orchestrator = None
    
    async def initialize(self):
        """Initialize orchestrator"""
        try:
            from orchestrator import ContentFactoryOrchestrator
            
            self.orchestrator = ContentFactoryOrchestrator(
                api_key=self.api_key,
                primary_model='gemini-2.5-flash'
            )
            await self.orchestrator.initialize()
            return True
        except Exception as e:
            st.error(f"Initialization failed: {str(e)}")
            return False
    
    async def generate_content(self, topic, platforms, brand_voice, progress_callback=None):
        """Generate content with progress updates"""
        try:
            session_id = f"web_{int(time.time())}"
            
            if progress_callback:
                progress_callback("Initializing agents...", 0.1)
            
            if not self.orchestrator:
                await self.initialize()
            
            if progress_callback:
                progress_callback("Loading brand voice...", 0.2)
            
            self.orchestrator.memory_bank.set('brand_voice', brand_voice)
            
            if progress_callback:
                progress_callback("Starting research...", 0.25)
            
            result = await self.orchestrator.create_content_package(
                topic=topic,
                session_id=session_id,
                platforms=platforms
            )
            
            if progress_callback:
                progress_callback("Saving outputs...", 0.95)
            
            await self.orchestrator.save_outputs(result, topic)
            
            if progress_callback:
                progress_callback("Complete!", 1.0)
            
            return result
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {str(e)[:50]}", 0.0)
            raise


def create_metrics_dashboard(metrics):
    """Create metrics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Word Count", metrics.get('blog_word_count', 0))
    with col2:
        st.metric("🎯 SEO Score", f"{metrics.get('seo_score', 0)}/100")
    with col3:
        st.metric("📖 Readability", f"{metrics.get('readability_score', 0):.0f}/100")
    with col4:
        st.metric("✅ Confidence", f"{metrics.get('verification_confidence', 0)}%")


def create_timing_chart(timings):
    """Create timing chart"""
    if not timings:
        return
    
    stages = []
    durations = []
    
    for stage, data in timings.items():
        if isinstance(data, dict):
            stages.append(stage.replace('_', ' ').title())
            durations.append(data.get('avg_seconds', 0))
    
    if stages:
        fig = go.Figure(data=[
            go.Bar(
                x=stages,
                y=durations,
                marker_color='rgb(102, 126, 234)',
                text=[f"{d:.2f}s" for d in durations],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="⏱️ Processing Time Breakdown",
            xaxis_title="Stage",
            yaxis_title="Time (seconds)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, width='stretch')


def create_quality_gauge(score, title):
    """Create quality gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=250)
    return fig


def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Content Factory AI</h1>
        <p>Multi-Agent Content Creation System</p>
        <small>Google/Kaggle 5-Day AI Agents Capstone Project</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=150)
        st.title("⚙️ Settings")
        
        # API Key check
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or 'your_' in api_key:
            st.error("⚠️ API Key not configured")
            st.info("Add GOOGLE_API_KEY to .env file")
            demo_mode = st.checkbox("Use Demo Mode", value=True)
            if not demo_mode:
                st.stop()
        else:
            st.success("✅ API Key configured")
            demo_mode = st.checkbox("Use Demo Mode", value=False)
        
        st.divider()
        
        # Brand Voice Management
        st.subheader("🎤 Brand Voice")
        
        from brand_voices import brand_voice_manager
        
        # Voice tabs
        voice_tab1, voice_tab2, voice_tab3 = st.tabs(["📚 Predefined", "✍️ Create", "💾 Saved"])
        
        with voice_tab1:
            st.write("**Select predefined voice:**")
            
            predefined_options = {
                'aggressive_consultant': '💥 Aggressive Consultant',
                'friendly_expert': '😊 Friendly Expert',
                'data_analyst': '📊 Data Analyst',
                'investigative_journalist': '🔍 Investigative Journalist',
                'pragmatic_practitioner': '🔧 Pragmatic Practitioner'
            }
            
            selected_predefined = st.selectbox(
                "Choose Voice",
                options=list(predefined_options.keys()),
                format_func=lambda x: predefined_options[x],
                index=4,
                key='predefined_voice'
            )
            
            predefined_voice = brand_voice_manager.get_voice(selected_predefined)
            st.info(f"**{predefined_voice['name']}**\n\n{predefined_voice['description']}")
            
            with st.expander("Voice Details"):
                st.write(f"**Tone:** {predefined_voice['tone']}")
                st.write(f"**Style:** {predefined_voice['style']}")
                st.write("**Examples:**")
                for ex in predefined_voice.get('examples', [])[:3]:
                    st.write(f"- {ex}")
            
            use_predefined = st.checkbox("Use this predefined voice", value=True, key='use_predefined')
        
        with voice_tab2:
            st.write("**Create custom voice:**")
            
            custom_voice_name = st.text_input(
                "Voice Name",
                placeholder="e.g., Tech Thought Leader",
                key='custom_name'
            )
            
            custom_voice_text = st.text_area(
                "Describe Your Brand Voice",
                placeholder="""Example:

I write as a seasoned technology executive with 20 years of experience. My tone is authoritative but approachable. I use industry insights, real-world examples, and strategic thinking. I challenge conventional wisdom with data-backed arguments. I avoid jargon and focus on practical, actionable advice. My style is direct, confident, and results-oriented.""",
                height=250,
                key='custom_text'
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Save Voice", key='save_voice'):
                    if custom_voice_name and custom_voice_text:
                        voice_id = custom_voice_name.lower().replace(' ', '_')
                        voice_data = brand_voice_manager.parse_voice_from_text(custom_voice_text)
                        voice_data['name'] = custom_voice_name
                        
                        if brand_voice_manager.save_custom_voice(voice_id, voice_data):
                            st.success(f"✅ Saved '{custom_voice_name}'!")
                            st.rerun()
                        else:
                            st.error("Failed to save voice")
                    else:
                        st.warning("Please provide name and description")
            
            with col2:
                if st.button("🧪 Preview", key='preview_voice'):
                    if custom_voice_text:
                        preview = brand_voice_manager.parse_voice_from_text(custom_voice_text)
                        st.write("**Parsed:**")
                        st.json({'tone': preview['tone']})
        
        with voice_tab3:
            st.write("**Saved voices:**")
            
            custom_voices = brand_voice_manager.load_custom_voices()
            
            if custom_voices:
                for voice_id, voice_data in custom_voices.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{voice_data['name']}**")
                        st.caption(voice_data.get('description', '')[:80] + '...')
                    with col2:
                        if st.button("🗑️", key=f'del_{voice_id}'):
                            if brand_voice_manager.delete_custom_voice(voice_id):
                                st.success("Deleted!")
                                st.rerun()
                    
                    if st.checkbox(f"Use '{voice_data['name']}'", key=f'use_{voice_id}'):
                        st.session_state['selected_custom_voice'] = voice_id
                        st.session_state['use_predefined'] = False
            else:
                st.info("No saved voices yet")
        
        st.divider()
        
        # Platform selection
        st.subheader("📱 Platforms")
        platforms = []
        if st.checkbox("Blog Post", value=True):
            platforms.append('blog')
        if st.checkbox("LinkedIn"):
            platforms.append('linkedin')
        if st.checkbox("Twitter"):
            platforms.append('twitter')
        if st.checkbox("Email Newsletter"):
            platforms.append('email')
        if st.checkbox("YouTube Script"):
            platforms.append('youtube')
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.info("""
        **Features:**
        - 🔍 Deep research
        - ✍️ Multi-platform content
        - ✅ Fact-checking
        - 📊 SEO optimization
        - 🎤 Custom brand voices
        """)
        
        # Stats
        if os.path.exists('memory/memory.json'):
            try:
                with open('memory/memory.json', 'r') as f:
                    memory = json.load(f)
                    history = memory.get('content_history', [])
                    if history:
                        st.metric("📈 Total Generated", len(history))
            except:
                pass
    
    # Determine selected voice
    if st.session_state.get('use_predefined', True):
        selected_voice = brand_voice_manager.get_voice(selected_predefined)
    elif 'selected_custom_voice' in st.session_state:
        selected_voice = brand_voice_manager.get_voice(st.session_state['selected_custom_voice'])
    else:
        selected_voice = brand_voice_manager.get_voice('pragmatic_practitioner')
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Generate", "📊 Analytics", "📁 History"])
    
    with tab1:
        st.header("Generate Content")
        
        topic = st.text_input(
            "📝 Enter Topic",
            placeholder="e.g., Future of AI Agents in 2025",
            value="Future of AI Agents in 2025"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"**Voice:** {selected_voice['name']} | **Platforms:** {', '.join(platforms) if platforms else 'None'}")
        
        with col2:
            generate_btn = st.button("🚀 Generate Content", type="primary")
        
        if generate_btn:
            if not topic:
                st.error("Please enter a topic")
            elif not platforms:
                st.error("Please select at least one platform")
            else:
                if demo_mode:
                    st.warning("⚠️ DEMO MODE")
                    with st.spinner("Generating demo..."):
                        time.sleep(2)
                        result = {
                            'blog': f"# {topic}\n\nDemo content in {selected_voice['name']} voice...",
                            'linkedin': 'Demo LinkedIn...',
                            'twitter': 'Demo Twitter...',
                            'email': 'Demo Email...',
                            'video_script': 'Demo Script...',
                            'verification': 'Demo verification',
                            'meta_description': topic,
                            'metrics': {
                                'duration_seconds': 2.0,
                                'blog_word_count': 150,
                                'seo_score': 85,
                                'readability_score': 88,
                                'verification_confidence': 95,
                                'sources_used': 10,
                                'flagged_claims': 0,
                                'keywords': {'primary': topic, 'secondary': []},
                                'timings': {}
                            },
                            'learned_insights': {}
                        }
                        st.success("✅ Demo generated!")
                else:
                    # Real generation
                    with st.status("Generating content...", expanded=True) as status:
                        st.write("🔧 Initializing...")
                        factory = StreamlitContentFactory()
                        
                        st.write("🔍 Researching...")
                        
                        try:
                            result = asyncio.run(
                                factory.generate_content(topic, platforms, selected_voice, None)
                            )
                            
                            st.write("✅ Complete!")
                            status.update(label="Content generated!", state="complete", expanded=False)
                            
                            if result:
                                st.success("✅ Success!")
                            else:
                                st.error("❌ Failed")
                                st.stop()
                                
                        except Exception as e:
                            status.update(label="Error", state="error")
                            st.error(f"Error: {str(e)}")
                            st.stop()
                
                # Display results
                if result:
                    st.divider()
                    st.header("📊 Results")
                    
                    create_metrics_dashboard(result['metrics'])
                    
                    st.divider()
                    
                    # Quality gauges
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            create_quality_gauge(result['metrics']['seo_score'], "SEO Score"),
                            width='stretch'
                        )
                    with col2:
                        st.plotly_chart(
                            create_quality_gauge(result['metrics']['readability_score'], "Readability"),
                            width='stretch'
                        )
                    
                    create_timing_chart(result['metrics'].get('timings', {}))
                    
                    st.divider()
                    
                    # Content tabs
                    content_tabs = st.tabs([p.title() for p in platforms])
                    
                    for i, platform in enumerate(platforms):
                        with content_tabs[i]:
                            content = result.get(platform, '')
                            if content:
                                st.text_area(
                                    f"{platform.title()} Content",
                                    content,
                                    height=400,
                                    key=f"content_{platform}"
                                )
                                
                                st.download_button(
                                    label=f"📥 Download {platform.title()}",
                                    data=content,
                                    file_name=f"{platform}_{topic.replace(' ', '_')[:30]}.txt",
                                    mime="text/plain",
                                    key=f"dl_{platform}"
                                )
                            else:
                                st.warning(f"No {platform} content")
                    
                    st.divider()
                    
                    with st.expander("🔍 Fact-Check Report"):
                        st.text_area("Verification", result.get('verification', 'N/A'), height=200)
                    
                    with st.expander("🔑 SEO Keywords"):
                        keywords = result['metrics'].get('keywords', {})
                        st.write(f"**Primary:** {keywords.get('primary', 'N/A')}")
                        if keywords.get('secondary'):
                            st.write(f"**Secondary:** {', '.join(keywords['secondary'][:10])}")
    
    with tab2:
        st.header("📊 Analytics Dashboard")
        
        if os.path.exists('memory/memory.json'):
            try:
                with open('memory/memory.json', 'r') as f:
                    memory = json.load(f)
                    history = memory.get('content_history', [])
                
                if history:
                    st.success(f"Found {len(history)} content pieces")
                    
                    word_counts = []
                    seo_scores = []
                    dates = []
                    
                    for item in history[-20:]:
                        metrics = item.get('metrics', {})
                        word_counts.append(metrics.get('blog_word_count', 0))
                        seo_scores.append(metrics.get('seo_score', 0))
                        dates.append(item.get('timestamp', '')[:10])
                    
                    if word_counts:
                        fig1 = px.line(x=dates, y=word_counts, title="Word Count Trend")
                        st.plotly_chart(fig1, width='stretch')
                        
                        fig2 = px.line(x=dates, y=seo_scores, title="SEO Score Trend")
                        st.plotly_chart(fig2, width='stretch')
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Avg Words", f"{sum(word_counts)/len(word_counts):.0f}")
                        with col2:
                            st.metric("Avg SEO", f"{sum(seo_scores)/len(seo_scores):.1f}")
                        with col3:
                            st.metric("Total", len(history))
                else:
                    st.info("No data yet")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("No analytics available")
    
    with tab3:
        st.header("📁 Content History")
        
        if os.path.exists('memory/memory.json'):
            try:
                with open('memory/memory.json', 'r') as f:
                    memory = json.load(f)
                    history = memory.get('content_history', [])
                
                if history:
                    for idx, item in enumerate(reversed(history[-10:])):
                        topic_name = item.get('topic', 'Untitled')
                        timestamp = item.get('timestamp', '')[:19]
                        metrics = item.get('metrics', {})
                        content = item.get('content', {})
                        
                        with st.expander(f"📄 {topic_name} - {timestamp}", expanded=False):
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Words", metrics.get('blog_word_count', 0))
                            with col2:
                                st.metric("SEO", f"{metrics.get('seo_score', 0)}/100")
                            with col3:
                                st.metric("Readability", f"{metrics.get('readability_score', 0):.0f}/100")
                            with col4:
                                st.metric("Confidence", f"{metrics.get('confidence', 0)}%")
                            
                            st.divider()
                            
                            if content:
                                available = [p for p in ['blog', 'linkedin', 'twitter', 'email', 'youtube'] if content.get(p)]
                                
                                if available:
                                    hist_tabs = st.tabs([p.title() for p in available])
                                    
                                    for i, platform in enumerate(available):
                                        with hist_tabs[i]:
                                            plat_content = content.get(platform, '')
                                            if plat_content:
                                                st.text_area(
                                                    f"{platform.title()}",
                                                    plat_content,
                                                    height=300,
                                                    key=f"hist_{idx}_{platform}"
                                                )
                                                
                                                st.download_button(
                                                    label=f"📥 Download",
                                                    data=plat_content,
                                                    file_name=f"{platform}_{topic_name.replace(' ', '_')[:20]}.txt",
                                                    mime="text/plain",
                                                    key=f"hist_dl_{idx}_{platform}"
                                                )
                            else:
                                st.info("Content not available")
                else:
                    st.info("No history yet")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("No history available")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>🤖 Content Factory AI - Built with Google ADK & Gemini</p>
        <p><small>Google/Kaggle 5-Day AI Agents Intensive Capstone Project</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()