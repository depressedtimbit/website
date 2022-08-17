
  const PostsEl = document.querySelector('.forum-container2');
  const loaderEl = document.querySelector('.loader');
  
  // get the posts from API
  const getPosts = async (page, limit) => {
      const API_URL = `http://api.checkhost.local:5000/v1/forum/posts?page=${page}&index=${limit}`;
      const response = await fetch(API_URL);
      // handle 404
      if (!response.ok) {
          throw new Error(`An error occurred: ${response.status}`);
      }
      return await response.json();
  }
  
  // show the posts
  const showPosts = (Posts) => {
      Posts.forEach(post => {
          const postEl = document.createElement('div');
          postEl.innerHTML = `
          <a>${post.username} at ${post.date}</a>
          <div class="forum-post">
            <div class="post-text">${post.data}</div>
          </div>
          
      `;
  
          PostsEl.appendChild(postEl);
      });
  };
  
  const hideLoader = () => {
      loaderEl.style.visibility = "hidden";
  };
  
  const showLoader = () => {
      loaderEl.style.visibility = "visible";
  };
  
  const hasMorePosts = (page, limit, total) => {
    console.log(page, limit, total)
      const startIndex = (page - 1) * limit + 1;
      return total === 0 || startIndex < total;
  };
  

  // load posts
  const loadposts = async (page, limit) => {
  
      // show the loader
      showLoader();
      // 0.5 second later
      setTimeout(async () => {
          try {
              // if having more posts to fetch
              if (hasMorePosts(page, limit, total)) {
                  // call the API to get posts
                  const response = await getPosts(page, limit);
                  // show posts
                  showPosts(response);
                  // update the total
                  total = response.length;
              }
          } catch (error) {
              console.log(error);
          } finally {
              hideLoader();
          }
      }, 500);
  
  };
  
  // control variables
  let currentPage = 0;
  const limit = 10;
  let total = 0;
  
  
  window.addEventListener('scroll', () => {
      const {
          scrollTop,
          scrollHeight,
          clientHeight
      } = document.documentElement;
      console.log(scrollTop + clientHeight, scrollHeight)
      console.log(hasMorePosts(currentPage, limit, total))
      if (scrollTop + clientHeight >= scrollHeight - 5 &&
          hasMorePosts(currentPage, limit, total)) {
          currentPage++;
          loadposts(currentPage, limit);
      }
  }, {
      passive: true
  });
  
  // initialize
  loadposts(currentPage, limit);


  // on call functions
  function deletePost(POST_ID) {
    const formData = new FormData()
    formData.set("postid", POST_ID)
    fetch("/delete-post", {
      method: "POST",
      body: formData,
    })
      .then(() => window.location.reload())
  }