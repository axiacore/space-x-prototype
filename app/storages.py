from django.contrib.staticfiles.apps import StaticFilesConfig
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class JSManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """Custom static files storage class that supports JavaScript module import aggregation."""

    support_js_module_import_aggregation = True


class CustomStaticFilesConfig(StaticFilesConfig):
    """Custom static files config class that uses the custom static files storage class."""

    ignore_patterns = tuple(StaticFilesConfig.ignore_patterns) + (
        'LICENSE',
        '*.py',
        '*.pyc',
        '*.ts',
        '*.txt',
        '*.md',
        '*.json',
        '*.scss',
        '*.less',
        '*.sass',
        '*.mts',
        '*.styl',
        '*.cjs',
        'tailwindcss',
        '@tailwindcss',
        'src/**',
        'node_modules/.pnpm/**',
        'node_modules/alpinejs/src/**',
    )
