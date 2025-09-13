//tag::outputPath[]
outputPath = 'build/docs'
//end::outputPath[]

//tag::sourceDir[]
sourceDir = "src/docs"
//end::sourceDir[]

//tag::mainConfigFile[]
mainConfigFile = 'arc42/arc42-template.adoc'
//end::mainConfigFile[]

//tag::inputFiles[]
inputFiles = [
  [file: 'arc42/arc42-template.adoc', formats: ['html','pdf','pptx']],
]
//end::inputFiles[]

//tag::taskInputsDirs[]
taskInputsDirs = ["${sourceDir}"]

taskInputsFiles = []
//end::taskInputsDirs[]

//tag::githubConfig[]
github = [:]
github.with {
    user = 'docToolchain'
    repository = 'AsciiDoc-MCP'
    branch = 'main'
    docRoot = 'src/docs'
}
//end::githubConfig[]

//tag::microsite[]
microsite = [:]
microsite.with {
    homePage = 'arc42/arc42-template.adoc'
    branchName = 'gh-pages'
    gitRepoUrl = 'https://github.com/docToolchain/AsciiDoc-MCP.git'
    title = 'AsciiDoc MCP Server Documentation'
    description = 'Model Context Protocol server for structured AsciiDoc document analysis'
    logoPath = ''
    googleAnalyticsId = ''
    favicon = ''
    socialButtons = true
    breadcrumb = true
    navigationControls = true
    search = true
    editPage = true
    tags = true
    tocLevels = 3
    enableEditOnGithub = true
    enableProjectInfo = true
    enableLastUpdated = true
    enableGitHubLink = true
    githubUrl = 'https://github.com/docToolchain/AsciiDoc-MCP'
    customCss = ''
    customJs = ''
    headerContent = ''
    footerContent = ''
    metaDescription = 'Documentation for the AsciiDoc MCP Server - A Model Context Protocol server that provides structured access to AsciiDoc documents for Large Language Models'
    keywords = 'AsciiDoc, MCP, Model Context Protocol, Documentation, LLM, AI'
    author = 'docToolchain Team'
    version = '0.1.0'
}
//end::microsite[]