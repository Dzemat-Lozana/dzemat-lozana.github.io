# Association Bosniaque de Lausanne Website

This is the official website for the Association Bosniaque de Lausanne, built with Hugo, TailwindCSS, and multilingual support.

## Features

- Static website built with [Hugo](https://gohugo.io/)
- Multilingual support (French and Bosnian)
- Responsive design with [TailwindCSS](https://tailwindcss.com/)
- Automatic deployment to GitHub Pages

## Prerequisites

To work on this website locally, you need to have the following installed:

- [Hugo](https://gohugo.io/getting-started/installing/) (Extended version recommended)
- [Node.js](https://nodejs.org/) (v14 or newer)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/association-bosniaque-lausanne/website.git
cd website
```

### Install Dependencies

```bash
npm install
```

### Run the Development Server

```bash
npm run dev
```

This will start a local development server at http://localhost:1313/ with hot-reloading enabled.

## Project Structure

```
.
├── archetypes/         # Template files for new content
├── assets/             # Source files that require processing (CSS, JS, etc.)
│   └── css/
│       └── main.css    # Main CSS file with TailwindCSS imports
├── content/            # Content files organized by language
│   ├── fr/             # French content
│   └── bs/             # Bosnian content
├── layouts/            # HTML templates
│   ├── _default/       # Default templates
│   └── partials/       # Reusable template parts
├── static/             # Static files (images, fonts, etc.)
├── config.yaml         # Hugo configuration
├── package.json        # Node.js dependencies and scripts
├── tailwind.config.js  # TailwindCSS configuration
└── postcss.config.js   # PostCSS configuration
```

## Multilingual Content

The website supports both French and Bosnian languages. Content is organized by language in the `content` directory:

- `content/fr/` - French content
- `content/bs/` - Bosnian content

### Adding New Content

To add a new page or post, create a Markdown file in both language directories with the same filename:

```bash
# For French
hugo new fr/posts/my-new-post.md

# For Bosnian
hugo new bs/posts/my-new-post.md
```

### Translation

Each content file should have a corresponding file in the other language directory with the same filename. This allows Hugo to link the translations together.

## Styling with TailwindCSS

The website uses TailwindCSS for styling. The main CSS file is located at `assets/css/main.css`.

To customize the design:

1. Edit the TailwindCSS configuration in `tailwind.config.js`
2. Add custom styles in `assets/css/main.css`
3. Use TailwindCSS utility classes directly in the HTML templates

## Deployment

The website is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment process is handled by GitHub Actions as defined in `.github/workflows/hugo.yml`.

### Manual Deployment

If you need to deploy manually:

```bash
npm run build
```

This will generate the static site in the `public` directory, which can then be deployed to any static hosting service.

## Adding New Features

### Creating a New Section

1. Create directories for the new section in both language content folders:
   ```bash
   mkdir -p content/fr/new-section content/bs/new-section
   ```

2. Add an `_index.md` file in each directory to define the section:
   ```bash
   # content/fr/new-section/_index.md
   ---
   title: "Nouvelle Section"
   date: 2025-04-22
   draft: false
   ---
   
   # content/bs/new-section/_index.md
   ---
   title: "Nova Sekcija"
   date: 2025-04-22
   draft: false
   ---
   ```

3. Create a custom layout for the section if needed:
   ```bash
   mkdir -p layouts/new-section
   touch layouts/new-section/list.html
   touch layouts/new-section/single.html
   ```

### Adding a Menu Item

Edit the `config.yaml` file to add a new menu item:

```yaml
menu:
  main:
    - identifier: home
      name: Home
      url: /
      weight: 1
    - identifier: new-section
      name: New Section
      url: /new-section/
      weight: 2
```

Add translations for each language:

```yaml
languages:
  fr:
    menu:
      main:
        - identifier: new-section
          name: Nouvelle Section
          url: /fr/new-section/
          weight: 2
  bs:
    menu:
      main:
        - identifier: new-section
          name: Nova Sekcija
          url: /bs/new-section/
          weight: 2
```

## Contributing

1. Create a new branch for your changes
2. Make your changes
3. Test locally with `npm run dev`
4. Commit and push your changes
5. Create a pull request

## License

[MIT License](LICENSE)