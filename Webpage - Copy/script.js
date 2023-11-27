$(document).ready(function () {
    // Load movieData from movie_data.js
    $.getScript('movie_data.js', function () {
        // Check if movieData is defined
        if (typeof movieData !== 'undefined' && Array.isArray(movieData)) {
            // Function to create a movie suggestion element
            function createMovieSuggestion(movie) {
                const suggestion = $(`
                    <div class="suggestion">
                        <span>${movie.title}</span>
                    </div>
                `);
                return suggestion;
            }

            // Function to create a movie element
            function createMovieElement(movie) {
                const movieElement = $(`
                    <div class="matching-movie">
                        <span>${movie.title}</span>
                    </div>
                `);
                return movieElement;
            }

            // Function to filter movies by selected genre
            function filterByGenre(selectedGenre) {
                const input = $('#movie-input').val().toLowerCase();
                const suggestionsContainer = $('#suggestions-container');
                suggestionsContainer.empty();

                // Filter movie data based on user input and selected genre
                const matchingTitles = movieData.filter(function (item) {
                    return (item[0].toLowerCase().includes(input) &&
                            (selectedGenre === '' || item[1].includes(selectedGenre)));
                });

                // Display suggestions
                matchingTitles.forEach(function (item) {
                    const suggestion = createMovieSuggestion({ title: item[0] });
                    suggestionsContainer.append(suggestion);
                });

                // Display matching movies based on the selected genre
                displayMatchingMovies(selectedGenre);
            }

            // Function to populate the genre dropdown
            function populateGenreDropdown() {
                const genreDropdown = $('#genre-dropdown');
                
                // Extract all unique genres from movieData
                const allGenres = [];
                movieData.forEach(function(item) {
                    item[1].split('|').forEach(function(genre) {
                        if (!allGenres.includes(genre)) {
                            allGenres.push(genre);
                            // Create an option element and add it to the dropdown
                            const option = $('<option></option>').val(genre).text(genre);
                            genreDropdown.append(option);
                        }
                    });
                });
            }

            // Function to display matching movies based on the selected genre
            function displayMatchingMovies(selectedGenre) {
                const matchingGenresContainer = $('#matching-genres-container');
                matchingGenresContainer.empty();

                let matchingMoviesCount = 0;

                movieData.forEach(function(item) {
                    if (item[1].includes(selectedGenre)) {
                        if (matchingMoviesCount < 10) {
                            const movieElement = createMovieElement({ title: item[0] });
                            matchingGenresContainer.append(movieElement);
                            matchingMoviesCount++;
                        }
                    }
                });
            }

            // Call the function to populate the genre dropdown when the page loads
            populateGenreDropdown();

            // Display movie suggestions
            const suggestionsContainer = $('#suggestions-container');
            $('#movie-input').on('input', function () {
                const input = $(this).val().toLowerCase();
                const selectedGenre = $('#genre-dropdown').val();
                suggestionsContainer.empty();

                // Filter movie data based on user input and selected genre
                const matchingTitles = movieData.filter(function (item) {
                    return (item[0].toLowerCase().includes(input) &&
                            (selectedGenre === '' || item[1].includes(selectedGenre)));
                });

                // Display suggestions
                matchingTitles.forEach(function (item) {
                    const suggestion = createMovieSuggestion({ title: item[0] });
                    suggestionsContainer.append(suggestion);
                });

                // Display matching movies based on the selected genre
                displayMatchingMovies(selectedGenre);
            });

            // Change event for the genre dropdown
            $('#genre-dropdown').on('change', function () {
                const selectedGenre = $(this).val();
                displayMatchingMovies(selectedGenre);
            });
        } else {
            console.error('movieData is not defined or is not an array.');
        }
    });
});