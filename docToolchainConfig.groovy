// Main config file for docToolchain
// Configuration for AsciiDoc-MCP project

// Root directory paths
outputPath = 'build/docs'
inputPath = 'src/docs'

// Input files to process
inputFiles = [
    [file: 'arc42/arc42.adoc', formats: ['html','pdf']],
]

// Directories containing images  
imageDirs = ["${inputPath}/images"]

// Project info
projectName = 'AsciiDoc-MCP'
projectTitle = 'AsciiDoc MCP Server - Model Context Protocol for AsciiDoc Documentation'

// GitHub configuration
github = [
    user: 'docToolchain',
    repository: 'AsciiDoc-MCP'
]

// Confluence settings (if needed later)
confluence = [
    spaceKey: 'ASCIIDOC-MCP',
    createSubpages: false,
    pagePrefix: '',
    pageSuffix: '',
    ancestorId: '',
    enableAttachments: true,
    extraPageContent: '',
    baseUrl: '',
    credentials: [
        username: '',
        password: ''
    ]
]

// Jira settings (if needed later)  
jira = [
    username: '',
    password: '',
    url: '',
    project: '',
    exports: []
]

// PlantUML settings
plantUML = [
    baseUrl: 'http://www.plantuml.com/plantuml',
    format: 'png'
]

// Asciidoctor attributes
asciidoctorAttributes = [
    'toc': 'left',
    'toclevels': '3',
    'sectnums': '',
    'icons': 'font',
    'source-highlighter': 'highlight.js',
    'imagesdir': 'images'
]