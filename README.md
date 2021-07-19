## What is this?
This is a static site generator for people who want a flexible but powerful way to build a personal website. It's only in `V0` and already has:
* A page generator which uses ONLY markdown
* Blog engine:
  * Pure Markdown
  * Automatic RSS Feeds
  * Automatic Text-To-Speech (TTS) for all posts
* A linktree-type page generator
* Add tasks to clone files from anywhere on the web before the engine starts rendering:
  * (even pair them with the page or blog engine, use them as if you already had them)
* A custom packing script (currently only supports HTML)
* <b>HAVE MULTIPLE INSTANCES FOR EACH KIND OF GENERATORS</b>


## How to use?
* Fork and deploy to vercel using this button:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https%3A%2F%2Fgithub.com%2Fayshptk%2Fblogengine&project-name=personalsite&repo-name=personalsite)

You will see something like this:
<img width="1440" alt="Screenshot 2021-07-19 at 3 21 41 PM" src="https://user-images.githubusercontent.com/62694274/126141723-152938c1-a31b-4fd2-b921-614732fe9feb.png">

* Click on dashboard and then go to project settings.
<img width="427" alt="Screenshot 2021-07-19 at 3 21 50 PM" src="https://user-images.githubusercontent.com/62694274/126141818-11da89c9-56a0-4090-b6ac-084a6594489c.png">

* 
* Scroll to `Build & Development Settings` in the `General` tab. And add these:
    * Build Command (override switch on): `sh deploy.sh`
    * Output Directory (override switch on): `.`
and then click on save.
<img width="783" alt="Screenshot 2021-07-19 at 3 22 26 PM" src="https://user-images.githubusercontent.com/62694274/126141988-3936ff93-b45e-4d2c-aad5-8ff0dc949a95.png">




* You define the type of engine to use for each directory in the `index.config.pagegen` file.
    * Use `blog` for each blog engine directory
    * Use `page` for each page engine directory
    * Use `links` for each links page directory
    * <b>Each command in a new line, followed by the name of the directory<b>
    * ^ an example page has already been included in the repo at `index.config.pagegen`
    * You can add any command you want to the `index.config.pagegen` file. The engine will run them in the order they are written.




# Detailed usage
## Page generator
This is the most basic generator. It uses markdown files and will generate a page for each markdown file in the directory. 

Say you have a directory named `p` which you assiged to the page generator. Then all the markdown files in `/p` will be rendered as pages. The rendered version for `/p/helloworld.md` will be available at `/p/helloworld` in the deployed site.The first line of each markdown file should be the title of the respective page. The engine is made with the idea of flexbility ground up. You can write your own template in `HTML` in the `template.pagegen` file and write `<!--[content]-->` wherever you want the rendered markdown to be inserted. Write `[[title]]` wherever you want the title of the page to be inserted. 

**Note** :While there is no need to have a `/p/index.md` file, it is recommended to have one.  

## Blog engine
Every directory you assign using the `blog` keyword will be handled by this part of the engine. Every directory of this type should have a `markdown` directory, an `index.html` file and a `template.pagegen` file. 

* The `index.html` file is the index of the blog. Feel free to add any content in the page and add `<!--[index]-->` wherever you want the posts to be listed. 
* The `template.pagegen` is the template for the blog. It is a `HTML` file. You can write your own template in it and write `<!--[content]-->` wherever you want the rendered markdown to be inserted. Write `[[title]]` wherever you want the title of the post to be inserted.
* The `markdown` directory should contain all the posts as markdown files. The files should be named using numbers. The first post <b>(oldest)</b> should be named `1.md`. And should be counted upwards towards the latest. The engine will take care of adding newest post to the top. That means if there are 20 posts. The post named `20.md` will be on top of the list in the `index.html` page.
* **Note** : while I find a better way to do this, the first line of each post should be the title of the post and the second line should be the date. Start writing the post from `line 3`.
* You also need a `{{{your directory}}}.config.pagegen` for each. I have already provided a template at `posts.config.pagegen`. The first three lines in the file are self explainatory, the fourth line is to specify whether you need the TTS narrated posts `slow` or `fast`.

#### The Magic
* Each blog directory has an auto-generated RSS feed called `feed.xml`
* Each blog post has an automatically generated TTS file embedded on the respective posts.
* All blog posts have auto-generated SEO friendly URLS.
* Your blog index is automatically managed
* All the HTML is automatically minified and thus the speed is increased.

## Tasks
This is a weird thing but I've always wanted to make shipping products really fast. I wrote this part of the engine to automatically convert the docs of all my side projects to HTML and deploy them to my own website. This is it! Here is how it works:
1. You link the raw markdown file from your side project's repo in the `tasks.json` file
2. You also give the name of the file it should be clonded as. (example given in the `tasks.json` file already, check it out 😉)
3. The engine will automatically clone the file from your side project's repo and then render it as HTML.

<b>BONUS: I even wrote [a little github action](https://github.com/ayshptk/blogengine-autodeploy/) to trigger deploy of personal site every time a new commit is pushed to any of the repos you clone pages from 👀.</b>


## Links page generator
This part is relatively simple. Takes the links in the `links.yaml` file and renders them as a page. It currently supports 4 types of elements:
* Text (use type `text`)
* Button (use type `link`)
* Tweet (use type `tweet`)
* Spotify (use type `spotify`)

An example structure of the `links.yaml` file is already written in the file. You can name each link element in the `links:` whatever you want. But each link should have a unique name and have 2 attributes inside it. The `t` attribute is the type of the element and the `v` attribute is the value of the element.

For Spotify and Tweet, the `v` attribute should be the URL of the profile/tweet/playlist. The embed codes are generated automatically. Remember to make your own template in `template.pagegen` in the directory and add `<!--[content]-->` wherever you want the links to be inserted.

