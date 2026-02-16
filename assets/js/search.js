/**
 * Recherche full-text côté client
 */
(function() {
  'use strict';
  
  let searchIndex = [];
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  if (!searchInput || !searchResults) return;
  
  // Charger l'index
  fetch('/search.json')
    .then(response => response.json())
    .then(data => {
      searchIndex = data;
      console.log(`✓ Index chargé: ${searchIndex.length} articles`);
    })
    .catch(error => console.error('Erreur chargement index:', error));
  
  // Recherche avec debounce
  let searchTimeout;
  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => search(this.value), 300);
  });
  
  function search(query) {
    if (!query || query.length < 2) {
      searchResults.innerHTML = '';
      searchResults.style.display = 'none';
      return;
    }
    
    query = query.toLowerCase();
    const words = query.split(/\s+/).filter(w => w.length > 1);
    
    const results = searchIndex.filter(post => {
      const searchText = (
        post.title + ' ' + 
        post.content + ' ' + 
        post.tags.join(' ')
      ).toLowerCase();
      
      return words.every(word => searchText.includes(word));
    });
    
    displayResults(results.slice(0, 10), query);
  }
  
  function displayResults(results, query) {
    searchResults.style.display = 'block';
    
    if (results.length === 0) {
      searchResults.innerHTML = `
        <div class="search-no-results">
          <p>Aucun résultat pour "<strong>${escapeHtml(query)}</strong>"</p>
        </div>
      `;
      return;
    }
    
    const html = `
      <div class="search-results-header">
        <p>${results.length} résultat${results.length > 1 ? 's' : ''}</p>
      </div>
      <div class="search-results-list">
        ${results.map(post => `
          <article class="search-result">
            <h3><a href="${post.url}">${highlightText(post.title, query)}</a></h3>
            <time>${formatDate(post.date)}</time>
            <p class="excerpt">${highlightText(post.excerpt, query)}</p>
            ${post.tags.length > 0 ? `
              <div class="tags">
                ${post.tags.slice(0, 5).map(tag => 
                  `<span class="tag">${tag}</span>`
                ).join('')}
              </div>
            ` : ''}
          </article>
        `).join('')}
      </div>
    `;
    
    searchResults.innerHTML = html;
  }
  
  function highlightText(text, query) {
    const words = query.toLowerCase().split(/\s+/).filter(w => w.length > 1);
    let result = escapeHtml(text);
    
    words.forEach(word => {
      const regex = new RegExp(`(${escapeRegex(word)})`, 'gi');
      result = result.replace(regex, '<mark>$1</mark>');
    });
    
    return result;
  }
  
  function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    });
  }
  
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.style.display = 'none';
    }
  });
  
  searchInput.addEventListener('focus', function() {
    if (searchResults.innerHTML) {
      searchResults.style.display = 'block';
    }
  });
})();
