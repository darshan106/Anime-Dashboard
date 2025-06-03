import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas

pn.extension('tabulator')

# Load and preprocess data
df = pd.read_csv('anime-dataset-2023.csv')
df = df.fillna(0)
df = df[~df.isin(['UNKNOWN']).any(axis=1)]
df['Genres'] = df['Genres'].str.split(',').str[0]

def extract_start_year(aired):
    if 'to' in aired:
        return int(aired.split(', ')[1].split(' ')[0])
    else:
        return int(aired.split(', ')[1])

df['Release'] = df['Aired'].apply(extract_start_year)

# Create interactive DataFrame
idf = df.interactive()

# Create widgets
year_slider = pn.widgets.IntSlider(name='Year slider', start=1960, end=2025, step=1, value=2000)
yaxis_anime = pn.widgets.RadioButtonGroup(name='Y axis', options=['Favorites', 'Popularity'], button_type='success')
yaxis_anime_genres = pn.widgets.RadioButtonGroup(name='Y axis', options=['Popularity', 'Favorites'], button_type='success')

# Define sources and genres
Sources = ['Manga', 'Light novel', 'Novel', 'Other']
genres_excl_world = ['Action', 'Adventure', 'Comedy', 'Drama', 'Sports', 'Award Winning', 'Sci-Fi', 'Horror', 
                     'Boys Love', 'Ecchi', 'Slice of Life', 'Fantasy', 'Avant Garde', 'Mystery', 'Supernatural', 
                     'Suspense', 'Romance', 'Gourmet', 'Girls Love']

# Data pipelines
anime_pipeline = (
    idf[
        (idf.Release <= year_slider) & 
        (idf.Source.isin(Sources))
    ]
    .groupby(['Source', 'Release'])[yaxis_anime].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='Release')
    .reset_index(drop=True)
)

def format_members(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return str(value)

score_vs_members_pipeline = (
    idf[
        (idf.Release <= year_slider) & 
        (idf.Source.isin(Sources))
    ]
    .groupby(['Source', 'Release', 'Score'])['Members']
    .mean()
    .to_frame()
    .reset_index()
    .assign(Members=lambda x: x['Members'].apply(format_members))
    .sort_values(by='Release')
    .reset_index(drop=True)
)

anime_genres_bar_pipeline = (
    idf[
        (idf.Release == year_slider) & 
        (idf.Genres.isin(genres_excl_world))
    ]
    .groupby(['Release', 'Genres'])[yaxis_anime_genres].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='Release')
    .reset_index(drop=True)
)

# Create plots and table
anime_plot = anime_pipeline.hvplot(x='Release', by='Source', y=yaxis_anime, line_width=2, 
                                  title="Favorites and Popularity over Release year by Sources")
anime_table = anime_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, 
                                 sizing_mode='stretch_width')
score_vs_members_scatterplot = score_vs_members_pipeline.hvplot(x='Score', y='Members', by='Source', 
                                                              size=79, kind='scatter', alpha=0.7, 
                                                              legend=False, height=500, width=500)
anime_genres_bar_plot = anime_genres_bar_pipeline.hvplot(kind='bar', x='Genres', y=yaxis_anime_genres, 
                                                       title='Popular and favorites anime release by genres')

# Create dashboard layout
template = pn.template.FastListTemplate(
    title='Anime Dashboard',
    sidebar=[
        pn.pane.Markdown("# Stats of Anime"),
        pn.pane.Markdown("#### Anime is a style of animation popular in Japanese films and television series. "
                        "It often combines stark, colorful graphics with action-packed plots. "
                        "Early anime films were intended primarily for a Japanese audience. "
                        "Therefore, they used many cultural references unique to Japan."),
        pn.pane.PNG('Kakashi.png', sizing_mode='scale_both'),
        pn.pane.Markdown("## Settings"),
        year_slider
    ],
    main=[
        pn.Row(
            pn.Column(yaxis_anime, anime_plot.panel(width=700), margin=(0,25)),
            anime_table.panel(width=500)
        ),
        pn.Row(
            pn.Column(score_vs_members_scatterplot.panel(width=600), margin=(0,25)),
            pn.Column(yaxis_anime_genres, anime_genres_bar_plot.panel(width=600))
        )
    ],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)

template.servable()