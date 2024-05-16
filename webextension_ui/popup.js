document.addEventListener('DOMContentLoaded', function () {
  // Get the current active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      // Get the loading element
      const loadingElement = document.getElementById('loading');
      // Show the loading animation
      // Display the URL of the active webpage
      loadingElement.style.display = 'block';
      const url = tabs[0].url;

      const data = {
          url: url
      };

      // Options for the fetch request
      const options = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      };
      try{
        // Send POST request
        fetch('http://127.0.0.1:8000/', options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle response data here
                // Access pos_data and neg_data from the response
                if (data.error) {
                  const err = data.error;
                  loadingElement.style.display = 'none';
                  const errorDiv = document.getElementById('error');
                  errorDiv.innerHTML += err;
                } else {
                  loadingElement.style.display = 'none';
                  const uniquePosData = new Set(data.pos_data);
                  const uniqueNegData = new Set(data.neg_data);
                  const posData = [...uniquePosData];
                  const negData = [...uniqueNegData];
                  const posPercent = data.pos_percent;
                  const negPercent = data.neg_percent;
                  const posPercentId = document.getElementById('pos');
                  const negPercentId = document.getElementById('neg');
                  const positiveId = document.getElementById('positive');
                  const negativeId = document.getElementById('negative');
                  positiveId.innerHTML += 'Positive Data: ';
                  negativeId.innerHTML += 'Negative Data: ';
                  posPercentId.innerHTML += "Positive Percent: ";
                  negPercentId.innerHTML += "Negative Percent: ";
                  const posId = document.getElementById('pos_percent');
                  posId.innerHTML += posPercent;
                  posId.classList.add('text-success');
                  const negId = document.getElementById('neg_percent');
                  negId.innerHTML += negPercent;
                  negId.classList.add('text-danger');

                  // Iterate over pos_data and display its contents
                  const posList = document.getElementById('pos-list');
                  posData.forEach(item => {
                      const li = document.createElement('li');
                      li.textContent = item;
                      li.role = 'alert';
                      li.classList.add('alert','alert-success', 'list-unstyled', 'm-1', 'p-2', 'text-break')
                      posList.appendChild(li);
                  });

                  // Iterate over neg_data and display its contents
                  const negList = document.getElementById('neg-list');
                  negData.forEach(item => {
                      const li = document.createElement('li');
                      li.textContent = item;
                      li.role = 'alert';
                      li.classList.add('alert','alert-danger', 'list-unstyled', 'm-1', 'p-2', 'text-break')
                      negList.appendChild(li);
                  });
                }
            })
            .catch(error => {
                // Handle errors here
                loadingElement.style.display = 'none';
                loadingElement.style.display = 'none';
                const errorDiv = document.getElementById('error');
                errorDiv.innerHTML += "Few websites stop unauthorized scraping for security reasons.";
                console.error('There was a problem with your fetch operation:', error);
            });
      } catch(error) {
        loadingElement.style.display = 'none';
        const errorDiv = document.getElementById('error');
        errorDiv.innerHTML += "This is not the problem with you. This is the problem from Server.";
      }

      // Execute content script to extract links from the webpage
  });
});
