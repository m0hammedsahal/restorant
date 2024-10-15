  // Get the Search button and Search Bar elements
  const searchBtn = document.getElementById('searchBtn');
  const searchBar = document.getElementById('searchBar');

  // Add click event listener to toggle the Search Bar
  searchBtn.addEventListener('click', function () {
    if (searchBar.classList.contains('hidden')) {
      searchBar.classList.remove('hidden');
      searchBar.classList.add('show');
    } else {
      searchBar.classList.remove('show');
      searchBar.classList.add('hidden');
    }
  });
