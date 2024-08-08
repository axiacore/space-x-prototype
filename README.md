# SpaceX Travel Insurance Prototype

Calculating the Future: SpaceX's Travel Insurance.

How much life insurance will cost for a trip to space? At [Axiacore](https://axiacore.com/), we developed an insurance calculator for SpaceX to provide tickets for space tourists. This case study details the development process, challenges in automating, and the consulting approach in the space travel industry.

🎥 Watch how it works: https://www.loom.com/share/f7c36ee573784920af5b7878e18214b4

## Overview
------------

The SpaceX Travel Insurance Prototype is a conversational AI-powered chat that assesses a client's psychological and physical conditions to determine their fitness for space travel. The chat is designed to ask general questions that help identify potential risks and provide a personalized insurance policy.

The chat uses the Army Physical Fitness Test (APFT) as a reference point to evaluate the client's physical condition. This test assesses an individual's physical fitness in four areas: push-ups, sit-ups, a 2-mile run, and a 1.5-mile ruck march.

To evaluate the client's psychological condition, the chat uses the short form of the International Positive and Negative Affect Schedule (I-PANAS). This widely used psychological assessment tool measures an individual's positive and negative emotions, providing valuable insights into their mental well-being.

The chat's assessment results are then fed into our custom InsuranceCalculator service, which uses the collected data to calculate a unique insurance value for each client. This value is based on the client's individual physical and psychological conditions, as well as other factors relevant to space travel. 

## Running the Prototype
-------------------------

### Python Packages
We use [rye](https://rye.astral.sh/) for Python packages. Follow the installation instructions [here](https://rye.astral.sh/guide/installation/#installing-rye).

After installation, run the following commands:

```
rye config --set-bool behavior.use-uv=true
rye run python manage.py runserver 0.0.0.0:8000
```

### JavaScript Packages
We use [pnpm](https://pnpm.io/) for JavaScript packages. Follow the installation instructions [here](https://pnpm.io/installation).

After installation, run the following command:

```
pnpm install && rye run python manage.py tailwind start
```

### Requirements
----------------

* An Openia account to add the `OPENAI_API_KEY` to the `settings.py` file.
* A `SECRET_KEY` in the `settings.py` file.

## Main Technologies
--------------------

Here's an improved version of the "Main Technologies" section:

## Main Technologies
--------------------

### Django
We use Django, a high-level Python web framework, as the foundation of our web application. Django provides a robust and scalable architecture, allowing us to quickly develop and deploy our prototype. Its modular design and extensive library of third-party packages make it an ideal choice for building complex web applications.

### Tailwind CSS
Tailwind CSS is a utility-first CSS framework that allows us to write more concise and maintainable CSS code. We use Tailwind to style our application, leveraging its pre-defined classes and utility functions to quickly create a visually appealing and responsive user interface.

### Alpine.js
Alpine.js is a lightweight JavaScript framework that provides a simple and intuitive way to create interactive web applications. We use Alpine to add dynamic behavior to our application, such as conditional rendering and event handling.

### HTMX
HTMX is a modern JavaScript library that provides a set of tools for building interactive web applications. We use HTMX to create reusable, modular components that can be easily composed together to build complex user interfaces. HTMX's focus on simplicity and ease of use makes it an ideal choice for building fast and efficient web applications.

### Rye
Rye is a Python package that provides a set of tools for building and deploying web applications. We use Rye to manage our application's dependencies, configure our environment, and run our application in development and production modes. Rye's simplicity and flexibility make it an ideal choice for building and deploying web applications.
