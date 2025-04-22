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
│   ├── css/
│   │   └── main.css    # Main CSS file with TailwindCSS imports
│   └── js/
│       └── main.js     # JavaScript for interactive elements
├── content/            # Content files with language suffixes
│   ├── _index.fr.md    # French home page
│   ├── _index.bs.md    # Bosnian home page
│   ├── about.fr.md     # French about page
│   ├── about.bs.md     # Bosnian about page
│   └── posts/          # Blog posts directory
│       ├── post1.fr.md # French post
│       └── post1.bs.md # Bosnian post
├── i18n/               # Translation files
│   ├── fr.yaml         # French translations
│   └── bs.yaml         # Bosnian translations
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

The website supports both French and Bosnian languages. Content is organized using language suffixes in filenames:

- `content/page.fr.md` - French version of a page
- `content/page.bs.md` - Bosnian version of a page

### Adding New Content

To add a new page or post, create Markdown files with language suffixes:

```bash
# For French
hugo new posts/my-new-post.fr.md

# For Bosnian
hugo new posts/my-new-post.bs.md
```

### Translation

Each content file should have a corresponding file with the same base name but different language suffix. This allows Hugo to link the translations together.

## Styling with TailwindCSS

The website uses TailwindCSS for styling. The main CSS file is located at `assets/css/main.css`.

To customize the design:

1. Edit the TailwindCSS configuration in `tailwind.config.js`
2. Add custom styles in `assets/css/main.css`
3. Use TailwindCSS utility classes directly in the HTML templates

## JavaScript Functionality

The website includes minimal JavaScript for interactive elements like the language dropdown menu. The main JavaScript file is located at `assets/js/main.js`.

To add new JavaScript functionality:

1. Edit the `assets/js/main.js` file or add new JavaScript files in the `assets/js/` directory
2. Import new JavaScript files in the `layouts/_default/baseof.html` template
3. Use event listeners and DOM manipulation for interactive elements

## Deployment

The website is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment process is handled by GitHub Actions as defined in `.github/workflows/hugo.yml`.

### GitHub Actions Workflow

The GitHub Actions workflow performs the following steps:

1. Checks out the repository code
2. Sets up Node.js and installs dependencies
3. Builds the TailwindCSS files
4. Sets up Hugo (extended version)
5. Builds the Hugo site
6. Deploys the built site to GitHub Pages

The workflow is configured to:
- Run on pushes to the `main` branch
- Run on pull requests (for testing)
- Allow manual triggering via the GitHub Actions UI

### Setting Up GitHub Pages

To set up GitHub Pages for your repository:

1. Go to your GitHub repository
2. Navigate to Settings > Pages
3. Under "Source", select "GitHub Actions"
4. Ensure the repository has the necessary permissions set in the workflow file

### Manual Deployment

If you need to deploy manually:

```bash
# Build TailwindCSS
npm run tailwind:build

# Build Hugo site
npm run build
```

This will generate the static site in the `public` directory, which can then be deployed to any static hosting service.

## Adding New Features

### Creating a New Section

1. Create a new section directory:
   ```bash
   mkdir -p content/new-section
   ```

2. Add index files with language suffixes:
   ```bash
   # content/new-section/_index.fr.md
   ---
   title: "Nouvelle Section"
   date: 2025-04-22
   draft: false
   ---
   
   # content/new-section/_index.bs.md
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

## Development Workflow

### Local Development

For the best development experience, run these commands in separate terminal windows:

```bash
# Terminal 1: Run TailwindCSS in watch mode
npm run tailwind:watch

# Terminal 2: Run Hugo server
npm run start
```

This setup will:
- Watch for changes to your TailwindCSS files and rebuild them automatically
- Run the Hugo server with hot reloading at http://localhost:55043
- Allow you to see changes to your content, templates, and styles in real-time

### Recommended Development Tools

- Visual Studio Code with extensions:
  - Hugo Language and Syntax Support
  - Tailwind CSS IntelliSense
  - YAML
  - ESLint
  - Prettier

### Testing

Before committing changes, always test your site by:
1. Running `npm run build` to ensure the production build works
2. Checking the site in multiple browsers (Chrome, Firefox, Safari, Edge)
3. Testing responsive layouts on different screen sizes
4. Validating both language versions of the site

## Contributing

1. Create a new branch for your changes
2. Make your changes
3. Test locally with the development workflow described above
4. Ensure all pages work in both languages
5. Commit and push your changes
6. Create a pull request with a clear description of your changes

## License

[MIT License](LICENSE)