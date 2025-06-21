import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="RoFacts - Romania Socio-Economic indicators",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        /* Remove default streamlit padding */
        .block-container {
            padding-top: 0rem;
            max-width: 1600px;
            margin: auto;
        }
        
        /* Page background */
        .stApp {
            background-color: #FDF8F0;
        }
        
        /* Main title styling - same blue as KPI numbers */
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4f7d8f;
            text-align: center;
            margin: 2rem 0 3rem 0;
        }
        
        .data-source {
            font-size: 0.9rem;
            color: #7A8B99;
            text-align: center;
            margin-top: 2rem;
            font-style: italic;
        }
        .chart-container {
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        /* Reduce space between rows */
        .row-gap-small {
            margin-top: -1rem;
            margin-bottom: 0.5rem;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #F8EFDE;
        }
        
        /* Navigation menu styling */
        .nav-menu {
            padding: 1rem 0;
        }
        
        .nav-item {
            padding: 0.5rem 1rem;
            margin: 0.2rem 0;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .nav-item:hover {
            background-color: #E5D5C1;
        }
        
        .nav-item.active {
            background-color: #4f7d8f;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# GDP Chart Generator
class RomaniaGDPAnalyzer:
    def __init__(self):
        self.color_background = '#F8EFDE'
        self.color_gdp = '#46C07a'
        self.color_arrow = '#FC8553'
        
    def create_gdp_plotly_chart(self, df):
        """Create a Plotly line chart matching the wage graph style"""
        fig = go.Figure()

        # Add GDP line trace
        fig.add_trace(go.Scatter(
            x=df['year'], 
            y=df['gdp_current_usd'] / 1e9,
            mode='lines+markers',
            name='GDP (Billions USD)',
            line=dict(color=self.color_gdp),
            hovertemplate='Year: %{x}<br>GDP: $%{y:.2f}B<extra></extra>'
        ))

        # Add vertical line for EU joining
        fig.add_vline(
            x=2007, 
            line_dash="dash", 
            line_color="#4f7d8f",
            line_width=2
        )

        # Add annotation for EU joining
        fig.add_annotation(
            x=2007,
            y=df['gdp_current_usd'].max() / 1e9 * 0.9,  # Position at 90% of max GDP height
            text="Romania joins EU",
            showarrow=False,  # Remove the arrow
            font=dict(color="black", size=10),
            xanchor='right',  # Right-align the text so it ends at the line
            yanchor='middle'
        )

        fig.update_layout(
            title='Romania GDP Evolution (1990-2025)',
            title_x=0.35,  # Center the title
            xaxis_title='Year',
            yaxis_title='GDP (Billions USD)',
            plot_bgcolor=self.color_background,
            paper_bgcolor=self.color_background,
            xaxis=dict(dtick=2),
            yaxis=dict(tickformat='.'),
            font=dict(family="Arial, sans-serif", size=12, color="black"),
            title_font=dict(size=16, color="black")
        )
        return fig

# Population Pyramid Functions
def create_population_pyramid():
    """
    Creates a clean, simple population pyramid showing percentages
    """
    # Define colors to match your existing graphs
    color_background = '#F8EFDE'
    color_male = '#4f7d8f'  # Blue for men
    color_female = '#c46e6e'  # Red for women
    
    # Read the data
    #file_path = r'C:\Users\Svitlana\OneDrive\RoFacts\mvp\data\population.xlsx'
    file_path = r'Data/population.xlsx'
    df = pd.read_excel(file_path)

    # Extract data from DataFrame
    age_groups = df['Age_group'].tolist()
    male_population = df['Male_Count'].tolist()
    female_population = df['Female_Count'].tolist()

    # Convert percentages if they're stored as decimals in Excel
    male_percentages = [p * 100 if p < 1 else p for p in df['Male_Percent'].tolist()]
    female_percentages = [p * 100 if p < 1 else p for p in df['Female_Percent'].tolist()]
    
    fig = go.Figure()
    
    # Add male population (left side, negative values for display)
    fig.add_trace(go.Bar(
        y=age_groups,
        x=[-p for p in male_percentages],  # Negative for left side
        name='Male',
        orientation='h',
        marker=dict(color=color_male),
        text=[f'{p:.1f}%' for p in male_percentages],
        textposition='inside',
        textfont=dict(color='white', size=10),
        hovertemplate=(
            '<b>%{y}</b><br>' +
            'Male: %{customdata[0]:,.0f} people (%{customdata[1]:.1f}%)<br>' +
            '<extra></extra>'
        ),
        customdata=list(zip(male_population, male_percentages)),
        hoverlabel=dict(bgcolor=color_male, font=dict(color='white')),
    ))
    
    # Add female population (right side)
    fig.add_trace(go.Bar(
        y=age_groups,
        x=female_percentages,
        name='Female',
        orientation='h',
        marker=dict(color=color_female),
        text=[f'{p:.1f}%' for p in female_percentages],
        textposition='inside',
        textfont=dict(color='white', size=10),
        hovertemplate=(
            '<b>%{y}</b><br>' +
            'Female: %{customdata[0]:,.0f} people (%{customdata[1]:.1f}%)<br>' +
            '<extra></extra>'
        ),
        customdata=list(zip(female_population, female_percentages)),
        hoverlabel=dict(bgcolor=color_female, font=dict(color='white')),
    ))
    
    # Calculate tick range
    max_percent = max(max(male_percentages), max(female_percentages))
    tick_range = max_percent * 1.1
    
    # Create custom tick values and labels (absolute values)
    tick_vals = []
    tick_labels = []
    
    # Create ticks at even integer intervals (0, 2, 4, 6, etc.)
    max_tick = int(max_percent) + 1
    if max_tick % 2 != 0:  # Make sure we have even numbers
        max_tick += 1
    
    for i in range(0, max_tick + 1, 2):  # Step by 2 to get even numbers
        # Add negative tick (left side)
        if i > 0:
            tick_vals.append(-i)
            tick_labels.append(f'{i}%')
        # Add center tick (0)
        if i == 0:
            tick_vals.append(0)
            tick_labels.append('0%')
        # Add positive tick (right side)
        if i > 0:
            tick_vals.append(i)
            tick_labels.append(f'{i}%')
    
    # Update layout
    fig.update_layout(
        title='Romania Population Pyramid 2023',
        title_x=0.35,  # Center the title
        xaxis=dict(
            title='Population (%)',
            range=[-tick_range, tick_range],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            tickfont=dict(color='black'),
            tickvals=tick_vals,
            ticktext=tick_labels
        ),
        yaxis=dict(
            title='Age Groups',
            categoryorder='array',
            categoryarray=age_groups[::-1],  # Reverse order so youngest is at bottom
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5,
            tickfont=dict(color='black')
        ),
        barmode='relative',
        bargap=0.1,
        plot_bgcolor=color_background,
        paper_bgcolor=color_background,
        font=dict(family='Arial, sans-serif', size=12, color='black'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            bgcolor=color_background,
            bordercolor="gray",
            borderwidth=1
        ),
        height=500,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    # Add gender labels
    fig.add_annotation(
        x=-tick_range*0.6,
        y=len(age_groups),
        text="Male",
        showarrow=False,
        font=dict(size=16, color=color_male, family='Arial Black'),
        xanchor='center'
    )
    
    fig.add_annotation(
        x=tick_range*0.6,
        y=len(age_groups),
        text="Female",
        showarrow=False,
        font=dict(size=16, color=color_female, family='Arial Black'),
        xanchor='center'
    )
    
    return fig

# Life Expectancy Functions
@st.cache_data
def load_life_expectancy_data():
    #file_path = r'C:\Users\Svitlana\OneDrive\RoFacts\mvp\data\life_expectancy.xlsx'
    file_path = r'Data/life_expectancy.xlsx'
    return pd.read_excel(file_path)

def create_life_expectancy_chart():
    """Create life expectancy chart for Streamlit with toggle functionality"""
    
    # Define colors matching your reference
    color_background = '#F8EFDE'
    color_male = '#4f7d8f'  # Blue for males
    color_female = '#c46e6e'  # Red for females
    color_total = '#46C07a'  # Green for total (using your wage color)
    
    df = load_life_expectancy_data()
    
    fig = go.Figure()
    
    # Prepare data
    male_data = df[df['Sex'] == 'Males']
    female_data = df[df['Sex'] == 'Females']
    total_data = df[df['Sex'] == 'Total']
    
    # Add all traces (we'll control visibility with buttons)
    if not male_data.empty:
        fig.add_trace(go.Scatter(
            x=male_data['Year'], 
            y=male_data['Life_Expectancy'],
            mode='lines+markers',
            name='Males',
            line=dict(color=color_male, width=3),
            marker=dict(size=6),
            visible=True
        ))
    
    if not female_data.empty:
        fig.add_trace(go.Scatter(
            x=female_data['Year'], 
            y=female_data['Life_Expectancy'],
            mode='lines+markers',
            name='Females',
            line=dict(color=color_female, width=3),
            marker=dict(size=6),
            visible=True
        ))
    
    if not total_data.empty:
        fig.add_trace(go.Scatter(
            x=total_data['Year'], 
            y=total_data['Life_Expectancy'],
            mode='lines+markers',
            name='Total',
            line=dict(color=color_total, width=3),
            marker=dict(size=6),
            visible=False
        ))
    
    # Update layout with your styling and buttons
    fig.update_layout(
        title='Romania Life Expectancy (1990-2023)',
        title_x=0.35,  # Center the title
        xaxis_title='Year',
        yaxis_title='Life Expectancy (Years)',
        plot_bgcolor=color_background,
        paper_bgcolor=color_background,
        xaxis=dict(
            dtick=2  # Show every 2 years
        ),
        yaxis=dict(
            tickformat='.1f'  # One decimal place
        ),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        hovermode='x unified',
        height=500,  # Match other charts
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        title_font=dict(size=16, color="black"),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True, True, False]}],
                        label="By Gender",
                        method="restyle"
                    ),
                    dict(
                        args=[{"visible": [False, False, True]}],
                        label="Total Only",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="center",
                y=1.08,  # Lowered from 1.15 to accommodate centered title
                yanchor="middle",
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                font=dict(size=12)
            ),
        ]
    )
    
    return fig

# Load wage data
@st.cache_data
def load_wage_data():
    #return pd.read_csv(r'C:\Users\Svitlana\OneDrive\RoFacts\mvp\data\real_wage.csv')
    return pd.read_csv(r'Data/real_wage.csv')

# Load GDP data from CSV instead of API
@st.cache_data
def load_gdp_data():
    #df = pd.read_csv(r'C:\Users\Svitlana\OneDrive\RoFacts\mvp\data\gdp.csv')
    df = pd.read_csv(r'Data/gdp.csv')
    df = df[(df['year'] >= 1990) & (df['year'] <= 2025)]
    df = df.sort_values('year')
    return df

# Sidebar Navigation
with st.sidebar:
    st.markdown("### Navigation")
    
    # Create navigation buttons
    menu_items = ['Home', 'Economy', 'Government spending', 'Health', 'Population', 'About']
    
    for item in menu_items:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.current_page = item

    # Add some spacing
    st.markdown("---")
    
    # Show current page indicator
    st.markdown(f"**Current Page:** {st.session_state.current_page}")

# Main content based on selected page
if st.session_state.current_page == 'Home':
    # Main title only - same blue color as KPI numbers
    st.markdown('<h1 class="main-title">RoFacts - Romania Socio-Economic indicators</h1>', unsafe_allow_html=True)

    # KPI Boxes
    st.markdown("""
    <style>
        .kpi-container {
            display: flex;
            justify-content: space-between;
            margin: 2rem 0;
            gap: 1rem;
        }
        .kpi-box {
            background-color: #F8EFDE;
            border: 1px solid #E5D5C1;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            flex: 1;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .kpi-value {
            font-size: 2.2rem;
            font-weight: bold;
            color: #4f7d8f;
            margin-bottom: 0.3rem;
            line-height: 1.1;
        }
        .kpi-label {
            font-size: 0.95rem;
            color: #5A6C7D;
            font-weight: 500;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load data for KPIs
    try:
        # Population (from most recent data available)
        population_2024 = "19.1M"
        
        # GDP per capita (calculate from GDP data)
        gdp_df = load_gdp_data()
        latest_gdp = gdp_df.iloc[-1]['gdp_current_usd'] / 1e9  # Latest GDP in billions
        gdp_per_capita = (latest_gdp * 1e9) / 19100000  # Approximate per capita
        gdp_per_capita_formatted = f"€{gdp_per_capita/1.1:,.0f}"  # Convert USD to EUR roughly with thousands separator
        
        # Latest wage (from wage data)
        wage_df = load_wage_data()
        latest_wage = wage_df.iloc[-1]['Real Average Wage (RON) - 2023 prices']
        wage_formatted = f"{latest_wage:,.0f} RON"
        
        # Latest life expectancy (from life expectancy data) 
        life_df = load_life_expectancy_data()
        latest_life_total = life_df[life_df['Sex'] == 'Total'].iloc[-1]['Life_Expectancy']
        life_formatted = f"{latest_life_total:.1f}"
        
    except Exception as e:
        # Fallback values if data loading fails
        population_2024 = "19.1M"
        gdp_per_capita_formatted = "€12,800"
        wage_formatted = "4,250 RON"
        life_formatted = "75.2"

    # Display KPI boxes
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-value">{population_2024}</div>
            <div class="kpi-label">Population (2024)</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-value">{gdp_per_capita_formatted}</div>
            <div class="kpi-label">GDP per Capita</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-value">{wage_formatted}</div>
            <div class="kpi-label">Real Average Wage (2023)</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-value">{life_formatted}</div>
            <div class="kpi-label">Life Expectancy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create 2x2 layout
    # First row - Real Wage Chart and GDP Chart
    col1, col2 = st.columns(2)

    # Top Left - Real Wage Chart
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            merged_df = load_wage_data()
            
            color_background = '#F8EFDE'
            color_wage = '#46C07a'
            color_arrow = '#FC8553'
            
            fig_wage = go.Figure()
            fig_wage.add_trace(go.Scatter(
                x=merged_df['Year'], 
                y=merged_df['Real Average Wage (RON) - 2023 prices'],
                mode='lines+markers',
                name='Real Wage',
                line=dict(color=color_wage)
            ))

            if 2005 in merged_df['Year'].values:
                wage_2005 = merged_df.loc[merged_df['Year'] == 2005, 'Real Average Wage (RON) - 2023 prices'].iloc[0]
                fig_wage.add_annotation(
                    x=2005, 
                    y=wage_2005,
                    text="The average real wage reached the 1991 level", 
                    showarrow=True,
                    font=dict(color="black", size=10),
                    arrowhead=2, 
                    arrowsize=1, 
                    arrowwidth=2, 
                    arrowcolor='#4f7d8f',  # Changed to male color (blue)
                    ax=-100, 
                    ay=-100
                )

            fig_wage.update_layout(
                title='Real Average Wage (1991-2023)',
                title_x=0.35,  # Center the title
                xaxis_title='Year',
                yaxis_title='Amount (RON)',
                plot_bgcolor=color_background,
                paper_bgcolor=color_background,
                xaxis=dict(dtick=4),
                yaxis=dict(tickformat='.'),
                height=500
            )

            st.plotly_chart(fig_wage, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading wage data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Top Right - GDP Chart
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            gdp_df = load_gdp_data()
            analyzer = RomaniaGDPAnalyzer()
            fig_gdp = analyzer.create_gdp_plotly_chart(gdp_df)
            fig_gdp.update_layout(height=500)
            st.plotly_chart(fig_gdp, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading GDP data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Second row - Population Pyramid and Life Expectancy Chart
    col3, col4 = st.columns(2)

    # Bottom Left - Population Pyramid
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            fig_pyramid = create_population_pyramid()
            st.plotly_chart(fig_pyramid, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading population data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Right - Life Expectancy Chart
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            fig_life_expectancy = create_life_expectancy_chart()
            st.plotly_chart(fig_life_expectancy, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading life expectancy data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'Economy':
    # Main title only - same blue color as KPI numbers
    st.markdown('<h1 class="main-title">Economy - Romania Socio-Economic indicators</h1>', unsafe_allow_html=True)

    # KPI Boxes
    st.markdown("""
    <style>
        .kpi-container {
            display: flex;
            justify-content: space-between;
            margin: 2rem 0;
            gap: 1rem;
        }
        .kpi-box {
            background-color: #F8EFDE;
            border: 1px solid #E5D5C1;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            flex: 1;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .kpi-value {
            font-size: 2.2rem;
            font-weight: bold;
            color: #4f7d8f;
            margin-bottom: 0.3rem;
            line-height: 1.1;
        }
        .kpi-label {
            font-size: 0.95rem;
            color: #5A6C7D;
            font-weight: 500;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load data for KPIs
    try:
        # Population (from most recent data available)
        population_2024 = "19.1M"
        
        # GDP per capita (calculate from GDP data)
        gdp_df = load_gdp_data()
        latest_gdp = gdp_df.iloc[-1]['gdp_current_usd'] / 1e9  # Latest GDP in billions
        gdp_per_capita = (latest_gdp * 1e9) / 19100000  # Approximate per capita
        gdp_per_capita_formatted = f"€{gdp_per_capita/1.1:,.0f}"  # Convert USD to EUR roughly with thousands separator
        
        # Latest wage (from wage data)
        wage_df = load_wage_data()
        latest_wage = wage_df.iloc[-1]['Real Average Wage (RON) - 2023 prices']
        wage_formatted = f"{latest_wage:,.0f} RON"
        
    except Exception as e:
        # Fallback values if data loading fails
        population_2024 = "19.1M"
        gdp_per_capita_formatted = "€12,800"
        wage_formatted = "4,250 RON"

    # Display KPI boxes
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-value">{population_2024}</div>
            <div class="kpi-label">Population (2024)</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-value">{gdp_per_capita_formatted}</div>
            <div class="kpi-label">GDP per Capita</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-value">{wage_formatted}</div>
            <div class="kpi-label">Real Average Wage (2023)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create 1x2 layout for Economy charts
    col1, col2 = st.columns(2)

    # Left - Real Wage Chart
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            merged_df = load_wage_data()
            
            color_background = '#F8EFDE'
            color_wage = '#46C07a'
            color_arrow = '#FC8553'
            
            fig_wage = go.Figure()
            fig_wage.add_trace(go.Scatter(
                x=merged_df['Year'], 
                y=merged_df['Real Average Wage (RON) - 2023 prices'],
                mode='lines+markers',
                name='Real Wage',
                line=dict(color=color_wage)
            ))

            if 2005 in merged_df['Year'].values:
                wage_2005 = merged_df.loc[merged_df['Year'] == 2005, 'Real Average Wage (RON) - 2023 prices'].iloc[0]
                fig_wage.add_annotation(
                    x=2005, 
                    y=wage_2005,
                    text="The average real wage reached the 1991 level", 
                    showarrow=True,
                    font=dict(color="black", size=10),
                    arrowhead=2, 
                    arrowsize=1, 
                    arrowwidth=2, 
                    arrowcolor='#4f7d8f',  # Changed to male color (blue)
                    ax=-100, 
                    ay=-100
                )

            fig_wage.update_layout(
                title='Real Average Wage (1991-2023)',
                title_x=0.35,  # Center the title
                xaxis_title='Year',
                yaxis_title='Amount (RON)',
                plot_bgcolor=color_background,
                paper_bgcolor=color_background,
                xaxis=dict(dtick=4),
                yaxis=dict(tickformat='.'),
                height=500
            )

            st.plotly_chart(fig_wage, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading wage data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Right - GDP Chart
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        try:
            gdp_df = load_gdp_data()
            analyzer = RomaniaGDPAnalyzer()
            fig_gdp = analyzer.create_gdp_plotly_chart(gdp_df)
            fig_gdp.update_layout(height=500)
            st.plotly_chart(fig_gdp, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading GDP data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'Government spending':
    st.markdown('<h1 class="main-title">Government Spending</h1>', unsafe_allow_html=True)
    st.info("Government spending data and visualizations will be added here.")
    
    # Placeholder content
    st.markdown("""
    ### Coming Soon
    This section will include:
    - Government budget allocation
    - Public spending trends
    - Infrastructure investments
    - Social spending analysis
    """)

elif st.session_state.current_page == 'Health':
    st.markdown('<h1 class="main-title">Health Indicators</h1>', unsafe_allow_html=True)
    
    # Health KPI
    try:
        life_df = load_life_expectancy_data()
        latest_life_total = life_df[life_df['Sex'] == 'Total'].iloc[-1]['Life_Expectancy']
        life_formatted = f"{latest_life_total:.1f}"
    except:
        life_formatted = "75.2"
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-value">{life_formatted}</div>
            <div class="kpi-label">Life Expectancy (Years)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Life Expectancy Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    try:
        fig_life_expectancy = create_life_expectancy_chart()
        st.plotly_chart(fig_life_expectancy, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading life expectancy data: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'Population':
    st.markdown('<h1 class="main-title">Population Demographics</h1>', unsafe_allow_html=True)
    
    # Population KPI
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-value">19.1M</div>
            <div class="kpi-label">Total Population (2024)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Population Pyramid
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    try:
        fig_pyramid = create_population_pyramid()
        st.plotly_chart(fig_pyramid, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading population data: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'About':
    st.markdown('<h1 class="main-title">About RoFacts</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### About This Dashboard
    
    RoFacts provides comprehensive insights into Romania's socio-economic development through interactive visualizations and key performance indicators.
    
    ### Data Coverage
    
    **Economy Section:**
    - Real wages adjusted for inflation (1991-2023)
    - GDP evolution showing economic growth (1990-2025)
    - Key economic milestones like EU accession in 2007
    
    **Health Section:**
    - Life expectancy trends by gender and overall (1990-2023)
    - Interactive toggles to view different demographic breakdowns
    
    **Population Section:**
    - Current population demographics with age and gender distribution
    - Population pyramid showing demographic structure and trends
    
    ### Key Insights
    
    - **Economic Recovery**: Real wages reached 1991 levels again in 2005, showing the economic recovery after the 1990s transition
    - **EU Integration**: Romania's EU accession in 2007 marked a significant milestone in economic development
    - **Demographic Trends**: The population pyramid reveals aging demographic patterns common in developed European countries
    - **Health Improvements**: Life expectancy has steadily improved over time, with women consistently showing higher life expectancy than men
    - **Transformation**: All indicators reflect Romania's successful transformation from a communist to a market economy
    
    ### Data Sources
    
    - **Romanian National Institute of Statistics (INS)**: Official source for wage, population, and life expectancy data
    - **World Bank**: GDP data from official World Bank databases
    - **Data Processing**: Real wages adjusted using Consumer Price Index to constant 2023 prices
    
    ### Technical Notes
    
    - All monetary values are properly adjusted for inflation
    - GDP figures shown in current US dollars
    - Population data reflects the most recent official demographic statistics
    - Life expectancy calculations follow standard demographic methodologies
    
    ### Future Enhancements
    
    Planned additions to RoFacts include:
    - Government spending analysis and budget allocation trends
    - Additional health indicators and healthcare system metrics
    - Regional demographic breakdowns
    - Comparative analysis with other EU countries
    """)

# Data sources footer (shown on all relevant pages)
if st.session_state.current_page in ['Home', 'Economy', 'Health', 'Population']:
    st.markdown('<p class="data-source">Data Sources: Romanian National Institute of Statistics (INS) for wage, population, and life expectancy data | GDP from World Bank API</p>', 
                unsafe_allow_html=True)