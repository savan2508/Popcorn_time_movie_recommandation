# Movie Recommendation System Project

## Project Overview
This project develops a comprehensive movie recommendation system that provides personalized movie suggestions based on user demographics and movie preferences. The system leverages various machine learning models to predict user preferences and recommend movies accordingly.

## Models Used

### 1. Genre Prediction Model
- **Description**: Predicts a user's preferred movie genres based on their demographic data.
- **Technologies**: Python, Scikit-learn
- **Usage**:
  - **Input**: User's demographic data (age, gender, occupation)
  - **Output**: Probabilities for each genre

### 2. Content-Based Filtering
- **Description**: Recommends movies by comparing the similarity between movie features such as genres and tags.
- **Technologies**: Python, TF-IDF, Cosine Similarity
- **Usage**:
  - **Input**: Movie ID or movie features
  - **Output**: List of recommended movies based on content similarity

## Backend Setup

#### IMPORTANT NOTE: Before running the backend and frontend, make sure to run the model training notebooks to generate the necessary models and encoders.

### Technologies
- **Framework**: Flask
- **Database**: Redis (for caching), PostgreSQL (optional for advanced data handling)
- **API Communication**: TMDB API for fetching real-time movie data

### Installation
1. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   TMDB_API_KEY=your_tmdb_api_key
   REDIS_URL=redis://localhost:6379/0
   DATABASE_URL=postgresql://user:password@localhost/db_name
4. **Run the application**:
   ```bash
    export FLASK_APP=app.py
    python app.py
    ```
5. Cashing with Redis
   - Use Redis for caching to store the results of expensive queries and avoid recomputing them.

## Frontend Setup
### Technologies
- **Framework**: React.js
- **State Management**: Redux
- **Styling**: Material-UI
- **API Communication**: Axios
- **Routing**: React Router
- **Authentication**: JWT
- **Form Handling**: Formik

### Installation
1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
2. **Environment Variables**:
3. **Run the application**:
   ```bash
   npm start
   ```
   
## Model Training
### Genre Prediction Model
1. **Data Collection**:
   - Download the [MovieLens dataset](https://grouplens.org/datasets/movielens/latest/).
   - The dataset contains user ratings, movie metadata, and user demographic data.
2. **Set up the environment**:
   ```bash
   cd machine_learning
   conda env create -f environment.yml
   conda activate popcorn_time
    ```
3. **Data Preprocessing**:
    - Put the dataset in the `data/raw` folder or change the path in the notebook.
4. **Training**:
    - Run the `data_preprocessing.ipynb` notebook to prepare the data for training.
    - The notebook will generate the processed data in the `data/processed` folder.
    - The processed data includes user demographic data and movie genres.
    - The notebook also generates the genre prediction model.
    - The model is saved in the `models` folder.
    - The notebook also generates the necessary encoders for transforming the data during inference such as `age_map.pkl`, `occupation_ohe.pkl`, `genre_columns.pkl`. 
    - These files are saved in the `models` folder.
    - Run the notebook `model_training.ipynb` to train the user movie recommendation model.
    - The notebook will generate the trained model in the `models` folder.
    - If you want to interact with the model, you can use the `model_testinge.ipynb` notebook.
5. **Model Evaluation**:
    - The notebook evaluates the model's performance using metrics such as accuracy, precision, recall, and F1-score.
    - The evaluation results are displayed at the end of the notebook.
6. **Data Visualization**:
    - The notebook visualizes the model's predictions using bar charts.
    - The visualizations are displayed at the end of the notebook and `ml_25_dataset_analysis.ipynb` notebook.

### Content-Based Filtering
1. **Model Overview**:
   - The content-based filtering model recommends movies based on the similarity between movie features such as genres and tags.
2. **Data Collection**:
   - Download the [MovieLens dataset](https://grouplens.org/datasets/movielens/latest/).
   - The dataset contains user ratings, movie metadata, and user demographic data.
3. **Model Training**:
   - Follow the steps in the Genre Prediction Model section to set up the environment and preprocess the data.
   - These steps will generate the necessary data for training the content-based filtering model.
   - The model will generate movie recommendations based on the similarity between movie features.
   - The model is saved in the `models` folder.
   - The notebook will generate cosine similarity matrices for movies based on genres and tags.

## Sources
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/latest/)
- [TMDB API](https://www.themoviedb.org/documentation/api)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Material-UI Documentation](https://mui.com/getting-started/installation/)


## Contribution
- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.