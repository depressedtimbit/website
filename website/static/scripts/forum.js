
  const PostsEl = document.querySelector('.forum-container2');
  const loaderEl = document.querySelector('.loader');
  const EocEL = document.querySelector('.EndofContent')
  var DateTime = luxon.DateTime;
  // get the posts from API
  const getPosts = async (page, limit, user_id) => {
      const API_URL = `http://api.checkhost.local:5000/v1/forum/posts?page=${page}&index=${limit}&user_id=${user_id}`;
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
          const postEl = document.createElement('article');
          console.log(post.date)
          postdatetime = DateTime.fromRFC2822(post.date);
          postEl.innerHTML = `
          <div class="user-img-container">
          <img src="${post.pfp}" class="user-img">
          </div>
         <div class="post-text-area">
          <a>${post.username} ${postdatetime.toRelative()}</a>
          <div class="post-text">${post.data}</div>
          </div>
          
      `;
          postEl.className = "forum-post"
          PostsEl.appendChild(postEl);
          
      });
  };
  
  const hideLoader = () => {
      loaderEl.style.visibility = "hidden";
  };
  
  const showLoader = () => {
      loaderEl.style.visibility = "visible";
  };

  const hideEOC = () => {
     EocEL.style.visibility = "hidden";
  }
  // load posts
  const loadposts = async (page, limit, user_id) => {
  
      // show the loader
      showLoader();
      // 0.5 second later
      setTimeout(async () => {
          try {
                  // call the API to get posts
                  const response = await getPosts(page, limit, user_id);
                  if (response === "end of content") 
                  {
                    hasPosts = false;
                    hideEOC();
                  }
                  else {
                    // show posts
                    showPosts(response);
                    // update the total
                    total = response.length;
                  }
                  
                  
          } catch (error) {
              console.log(error);
          } finally {
              hideLoader();
              loadlock = true;
          }
      }, 500);
      
  };
  
  // control variables
  let currentPage = 0;
  const limit = 7;
  let total = 0;
  var hasPosts = true;
  var loadlock = false;
const init = async (user_id) => {
    // initialize
    loadposts(currentPage, limit, user_id);
    window.addEventListener('scroll', () => {
          const {
              scrollTop,
             scrollHeight,
            clientHeight
          } = document.documentElement;
          console.log(scrollTop + clientHeight, scrollHeight)
          //console.log(hasMorePosts(currentPage, limit, total))
          
          console.log(loadlock, hasPosts, currentPage)
        if (scrollTop + clientHeight >= scrollHeight - 5 && loadlock && hasPosts) {
                currentPage++;
                loadposts(currentPage, limit, user_id);
                
                console.log('Loaded posts');
                loadlock = false;
      }
  }, {
      passive: true
  });
}



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
