# Anime Dashboard

This Jupyter Notebook-based dashboard provides insights into anime data using Panel, HoloViews, and Tabulator in JupyterLab.

#### Instructions:

1. **Install Dependencies:**
    - Ensure you have Python installed on your system.
    - Clone this repository.
    - Navigate to the repository directory and create a virtual environment:

    ```bash
    python3 -m venv env
    ```

    - Activate the virtual environment:

    ```bash
    source env/bin/activate  # For Linux/Mac
    env\Scripts\activate.bat  # For Windows
    ```

    - Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Notebook:**
    - Launch JupyterLab:

    ```bash
    jupyter lab
    ```

    - Open the `Anime.py` notebook from the JupyterLab interface.

3. **Explore the Dashboard:**
    - Run the notebook cells to load the data and generate the dashboard.
    - Interact with the widgets and plots to explore the anime dataset.

#### Dashboard Image:

![Anime Dashboard](Dashboard.png)

#### Serving the Dashboard Locally:

To serve the dashboard locally, use the command:

```bash
panel serve Interactive_dashboard.py
```

#### Dataset:

- The dataset used for this dashboard is provided in `anime-dataset-2023.csv`.

## YouTube Demo:

For a video walkthrough of the dashboard, watch it here:

[![Anime Dashboard YouTube Demo](THUMBNAIL.png)](https://youtu.be/-T31Thgfz-k?si=cUWNCUy3EIDFjv0k)

#### Additional Notes:

- Ensure you have the necessary plugins and extensions installed in JupyterLab to support Panel, HoloViews, and Tabulator for the best viewing experience.
