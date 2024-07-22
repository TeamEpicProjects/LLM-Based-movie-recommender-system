# Movie Recommender System Documentation

## Project Overview

### Problem Statement
The goal of this project is to develop a movie recommender system that provides personalized movie recommendations to users based on their preferences for TV series. The system should filter recommendations by genre, popularity, and language, and also use an advanced language model to suggest movies with similar plot overviews to the user's favorite TV series.

### Tech Stack
- **Programming Language**: Python
- **Web Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Machine Learning Model**: Llama3-8B by OpenAI, deployed on Groq hardware
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Virtual Environment**: venv
- **Task Scheduling**: cron

### Dataset
- **TV Series Dataset**: Contains preprocessed data of various TV series.
- **Movies Dataset**: Contains preprocessed data of various movies.

Both datasets include the following columns:
- `adult`
- `backdrop_path`
- `id`
- `overview`
- `popularity`
- `poster_path`
- `release_date` / `first_air_date`
- `title` / `name`
- `vote_average`
- `vote_count`
- `genre_names`
- `language`

### Data Source
- **TMDB API**: Data for TV series and movies was fetched using the TMDB (The Movie Database) API. This API provides comprehensive information about movies, TV shows, and actors.

### System Workflow
1. **Data Loading and Preparation**:
   - Load preprocessed datasets for TV series and movies.
   - Ensure necessary columns (`adult` and `overview`) are present.
   - Add an `age_appropriate` column based on the `adult` field.

2. **User Input**:
   - Users provide their preferences via a Streamlit interface, including language, genres, popularity threshold, and favorite TV series.

3. **Filtering Based on Preferences**:
   - Filter movies based on user-defined criteria such as genre, popularity, and language.

4. **Advanced Filtering with Llama3-8B Model**:
   - Use the Llama3-8B model to generate movie recommendations based on the overviews of the user's favorite TV series.
   - Formulate a prompt that includes the overviews of the selected TV series and obtain recommendations from the model.

5. **Recommendation Output**:
   - Display the top movie recommendations to the user, including movie titles, overviews, genres, and popularity.

### Additional Components

#### Docker
- **Containerization**: The entire application, including the Streamlit interface, data processing, and model integration, is containerized using Docker. This ensures consistency across different environments and simplifies deployment.
- **Dockerfile**: A `Dockerfile` is used to set up the Python environment, install dependencies, and configure the application.

#### GitHub Actions
- **CI/CD**: GitHub Actions is used to automate the CI/CD pipeline. This includes tasks such as running tests, building Docker images, and deploying the application.
- **Workflow Configuration**: A `.github/workflows` directory contains the YAML files that define the CI/CD workflows.

#### venv
- **Virtual Environment**: `venv` is used to create isolated Python environments. This helps in managing dependencies and avoiding conflicts with system-wide packages.
- **Setup**: The virtual environment is set up in the development environment to install and manage project-specific dependencies.

#### cron
- **Task Scheduling**: `cron` is used to schedule periodic tasks such as data fetching and preprocessing. This ensures that the datasets are updated regularly.
- **Cron Jobs**: A `crontab` file is used to define the schedule for running the data fetching script on a monthly basis.

### End Result
The recommender system successfully integrates genre, popularity, and language filtering with the Llama3-8B model to provide personalized movie recommendations. By leveraging advanced language processing capabilities, the system can suggest movies with plot overviews similar to the user's favorite TV series, enhancing the relevance and personalization of the recommendations. The usage of Docker, GitHub Actions, venv, and cron ensures a robust, scalable, and maintainable application.

![Preview](https://raw.githubusercontent.com/username/project/master/image-path/image.png)
