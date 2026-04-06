# README via AI

## glennjlea.com

Personal website for **Glenn J Lea** — Senior Technical Writer and Canadian history enthusiast based in Berlin, Germany. The site serves as supporting material for his Substack newsletter, _The Story of Canada: Beyond Brant and Brock_, a serialized, chronological retelling of Canadian history.

🌐 **Live site:** [glennjlea.com](https://glennjlea.com/)\
📰 **Substack:** [glennjlea.substack.com](https://glennjlea.substack.com/)\
💼 **LinkedIn:** [linkedin.com/in/glennjlea](https://www.linkedin.com/in/glennjlea)

***

### About the Project

_Beyond Brant and Brock_ explores how Canada developed — from the St. Lawrence Iroquois to the founding of Upper Canada and beyond. The site accompanies Glenn's Substack series, providing reference material, images, and context for each article.

The project is built on the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) Jekyll theme.

***

### Features

* Static site built with **Jekyll** and the **Minimal Mistakes** theme
* Blog posts organized by date with archive support
* About page with author biography and project background
* Responsive design suitable for desktop and mobile
* Integration with the Beyond Brant and Brock Substack

***

### Getting Started

#### Prerequisites

* [Ruby](https://www.ruby-lang.org/) (version 2.5 or higher)
* [Bundler](https://bundler.io/)
* [Jekyll](https://jekyllrb.com/)

#### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/glennlea1525/glennjlea-com.git
    cd glennjlea-com
    ```
2.  Install dependencies:

    ```bash
    bundle install
    ```
3.  Serve the site locally:

    ```bash
    bundle exec jekyll serve
    ```
4. Open your browser and go to `http://localhost:4000`

***

### Project Structure

```
glennjlea-com/
├── _posts/         # Blog posts in Markdown
├── _pages/         # Static pages (About, Archives, etc.)
├── _data/          # Site configuration data
├── _includes/      # Reusable HTML partials
├── _layouts/       # Page layout templates
├── images/         # Image assets
├── _config.yml     # Jekyll site configuration
└── Gemfile         # Ruby gem dependencies
```

***

### Configuration

Site settings are managed in `_config.yml`. Key fields include:

* `title` — Site name
* `url` — Base URL of the live site
* `author` — Author name and social links
* `description` — Site description for SEO

***

### Writing a New Post

Create a new Markdown file in the `_posts/` directory following the naming convention:

```
YYYY-MM-DD-title-of-post.md
```

Add front matter at the top of the file:

```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD
categories:
  - history
tags:
  - canada
---
```

***

### Deployment

The site is deployed as a static site. After building, upload the contents of the `_site/` directory to your web host, or use a platform such as GitHub Pages or Netlify.

To build for production:

```bash
bundle exec jekyll build
```

***

### Credits

* **Author:** Glenn J Lea
* **Development:** [Lesslie Sosa](https://www.linkedin.com/in/lesslie-sosa)
* **Theme:** [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) by Michael Rose

***

### License

© 2019–2026 Glenn J Lea. All rights reserved.
