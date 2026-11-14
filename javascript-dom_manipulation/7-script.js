fetch('https://swapi-api.hbtn.io/api/films/?format=json')
  .then((response) => response.json())
  .then((data) => {
    const movies = document.querySelector('#list_movies');
    data.results.forEach((movie) => {
      const item = document.createElement('li');
      item.textContent = movie.title;
      movies.appendChild(item);
    });
  });
