# Lollms Tools Zoo

<p align="center">
  <img src="icon.png" alt="LCP Tools Icon" width="200"/>
</p>

[![License](https://img.shields.io/github/license/ParisNeo/lollms_tools_zoo)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/ParisNeo/lollms_tools_zoo.svg?style=social&label=Star)](https://github.com/ParisNeo/lollms_tools_zoo/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ParisNeo/lollms_tools_zoo.svg?style=social&label=Fork)](https://github.com/ParisNeo/lollms_tools_zoo/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/ParisNeo/lollms_tools_zoo.svg)](https://github.com/ParisNeo/lollms_tools_zoo/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ParisNeo/lollms_tools_zoo.svg)](https://github.com/ParisNeo/lollms_tools_zoo/pulls)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/ParisNeo/lollms_tools_zoo/graphs/commit-activity)
[![LCP Compatible](https://img.shields.io/badge/LCP-Compatible-brightgreen.svg)](doc/README.md)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ParisNeo/lollms_tools_zoo&type=Date)](https://star-history.com/#ParisNeo/lollms_tools_zoo&Date)

> **Note**: If you find this repository useful, please consider giving it a star! ⭐ It helps the project grow and motivates continued development.

## 📁 Repository Structure

```
lollms_tools_zoo/
├── tools/
│   ├── file_management/
│   │   └── file_manager.py          # File and directory operations
│   ├── text_processing/
│   │   └── text_processor.py        # Text manipulation and analysis
│   ├── math_calculator/
│   │   └── math_calculator.py       # Mathematical operations and statistics
│   ├── system_info/
│   │   └── system_info.py           # System and environment information
│   ├── bibliography/
│   │   ├── arxiv/
│   │   │   ├── arxiv_tools.py       # arXiv search, download, and organization
│   │   │   └── README.md            # arXiv tools documentation
│   │   ├── doi/
│   │   │   ├── doi_tools.py         # DOI and Crossref integration
│   │   │   └── README.md            # DOI tools documentation
│   │   ├── zotero/
│   │   │   ├── zotero_tools.py      # Zotero local and remote integration
│   │   │   └── README.md            # Zotero tools documentation
│   │   ├── bib_manager.py           # Bibliography management utilities
│   │   ├── README.md                # Bibliography tools overview
│   │   └── .env.example             # Environment configuration template
│   └── README.md                     # Tools documentation
├── doc/
│   └── README.md                     # LCP protocol documentation
└── README.md                         # This file
```

## 🚀 Available Toolsets

### 📂 File Management (`tools/file_management/`)
Comprehensive file and directory operations:
- `tool_list_directory` - List files and directories with pattern filtering
- `tool_read_file` - Read file contents with encoding support
- `tool_write_file` - Write content to files with auto-directory creation
- `tool_copy_file` - Copy files with overwrite protection
- `tool_move_file` - Move/rename files safely
- `tool_delete_file` - Delete files with confirmation requirement
- `tool_get_file_info` - Get detailed file metadata

### 📝 Text Processing (`tools/text_processing/`)
Text manipulation and analysis utilities:
- `tool_count_words` - Count words, characters, lines, and paragraphs
- `tool_find_replace` - Find and replace with case-sensitivity options
- `tool_extract_emails` - Extract email addresses from text
- `tool_extract_urls` - Extract URLs from text
- `tool_text_statistics` - Detailed text statistics and word frequency
- `tool_to_uppercase` / `tool_to_lowercase` / `tool_to_title_case` - Case conversion
- `tool_reverse_text` - Reverse text
- `tool_remove_whitespace` - Remove whitespace with multiple modes

### 🔢 Math Calculator (`tools/math_calculator/`)
Mathematical operations and statistical calculations:
- Basic operations: `tool_add`, `tool_subtract`, `tool_multiply`, `tool_divide`
- Advanced operations: `tool_power`, `tool_square_root`, `tool_factorial`
- Statistics: `tool_calculate_mean`, `tool_calculate_median`, `tool_calculate_std_dev`
- Utilities: `tool_calculate_percentage`

### 💻 System Information (`tools/system_info/`)
System and environment information:
- `tool_get_system_info` - Comprehensive system information
- `tool_get_current_directory` - Get current working directory
- `tool_get_environment_variable` - Get specific environment variable
- `tool_list_environment_variables` - List all environment variables with filtering
- `tool_get_disk_usage` - Disk usage statistics
- `tool_get_python_path` - Python executable and path information

### 📚 Bibliography & Research (`tools/bibliography/`)
Academic research and bibliography management tools:

#### arXiv Tools (`tools/bibliography/arxiv/`)
- `tool_search_arxiv` - Search arXiv papers by query, author, or category
- `tool_get_arxiv_paper` - Get detailed paper information by arXiv ID
- `tool_download_arxiv_pdf` - Download PDF from arXiv
- `tool_get_arxiv_citations` - Get citation information for a paper
- `tool_organize_arxiv_papers` - Organize downloaded papers by category/author

#### DOI & Crossref Tools (`tools/bibliography/doi/`)
- `tool_resolve_doi` - Resolve DOI to get publication metadata
- `tool_search_crossref` - Search Crossref database for publications
- `tool_get_citation_by_doi` - Get formatted citation from DOI
- `tool_validate_doi` - Validate DOI format and existence

#### Zotero Integration (`tools/bibliography/zotero/`)
- **Local Zotero** (no API key required):
  - `tool_zotero_local_search` - Search local Zotero library
  - `tool_zotero_local_get_item` - Get item details from local library
  - `tool_zotero_local_export` - Export items to BibTeX/JSON
- **Remote Zotero** (requires API key):
  - `tool_zotero_remote_search` - Search Zotero cloud library
  - `tool_zotero_remote_add_item` - Add items to Zotero library
  - `tool_zotero_remote_sync` - Sync local and remote libraries

#### Bibliography Manager (`tools/bibliography/bib_manager.py`)
- `tool_create_bibliography` - Create new bibliography database
- `tool_add_reference` - Add reference to bibliography
- `tool_search_references` - Search references by various criteria
- `tool_export_bibliography` - Export to BibTeX, JSON, or CSV
- `tool_import_bibliography` - Import from BibTeX, JSON, or CSV
- `tool_generate_citation` - Generate formatted citations (APA, MLA, Chicago, etc.)

## 🔧 Usage with Lollms

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/lollms_tools_zoo.git
```

2. Configure Lollms to use these tools:

```python
from lollms_client import LollmsClient
from pathlib import Path

client = LollmsClient(
    llm_binding_name="ollama",
    llm_binding_config={"model_name": "gemma4:e2b"},
    tools_binding_name="lcp",
    tools_binding_config={
        "tools_folders": [
            str(Path("lollms_tools_zoo/tools/file_management")),
            str(Path("lollms_tools_zoo/tools/text_processing")),
            str(Path("lollms_tools_zoo/tools/math_calculator")),
            str(Path("lollms_tools_zoo/tools/system_info")),
            str(Path("lollms_tools_zoo/tools/bibliography/arxiv")),
            str(Path("lollms_tools_zoo/tools/bibliography/doi")),
            str(Path("lollms_tools_zoo/tools/bibliography/zotero")),
        ]
    }
)
```

### Using Specific Toolsets

You can selectively load only the toolsets you need:

```python
# Load only bibliography tools
client = LollmsClient(
    # ... other config ...
    tools_binding_config={
        "tools_folders": [
            str(Path("lollms_tools_zoo/tools/bibliography/arxiv")),
            str(Path("lollms_tools_zoo/tools/bibliography/doi")),
        ]
    }
)
```

### Environment Configuration

Some tools require API keys or configuration. Create a `.env` file in the `tools/bibliography/` directory:

```bash
# Copy the example file
cp tools/bibliography/.env.example tools/bibliography/.env
```

Edit `.env` with your credentials:

```env
# Zotero Remote API Configuration
ZOTERO_API_KEY=your_zotero_api_key_here
ZOTERO_USER_ID=your_zotero_user_id_here
ZOTERO_LIBRARY_TYPE=user  # or 'group'

# Optional: Custom Zotero local database path
ZOTERO_LOCAL_DB_PATH=/path/to/zotero.sqlite
```

See [tools/bibliography/.env.example](tools/bibliography/.env.example) for a complete template.

## 📖 LCP Tool Format

All tools in this repository follow the LCP (LollmsCommunicationProtocol) format:

- **Function naming**: All tool functions start with `tool_`
- **Type hints**: Full type annotations for all parameters
- **Docstrings**: Google-style docstrings with Args and Returns sections
- **Return format**: All tools return dictionaries with `success` key
- **Error handling**: Comprehensive error handling with descriptive messages
- **Initialization**: Each toolset includes `init_tools_library()` for lazy loading

### Example Tool Structure

```python
def tool_example(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what the tool does.

    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2. Defaults to 10.

    Returns:
        dict: Dictionary containing results.
    """
    try:
        # Tool logic here
        result = param1 * param2
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }
```

## 📚 Bibliography Tools Documentation

Each bibliography sub-toolset has its own detailed README:

- [arXiv Tools Documentation](tools/bibliography/arxiv/README.md) - Search, download, and organize arXiv papers
- [DOI Tools Documentation](tools/bibliography/doi/README.md) - DOI resolution and Crossref integration
- [Zotero Tools Documentation](tools/bibliography/zotero/README.md) - Local and remote Zotero library management
- [Bibliography Overview](tools/bibliography/README.md) - Complete bibliography tools guide

## 🤝 Contributing

Contributions are welcome! To add new tools:

1. Choose the appropriate category folder (or create a new one)
2. Follow the LCP tool format guidelines
3. Include comprehensive docstrings
4. Add error handling
5. Include `init_tools_library()` function
6. Create a README.md for your toolset
7. Update this README with your new tools

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🔗 Related Documentation

- [LCP Protocol Documentation](doc/README.md) - Detailed LCP specification
- [Lollms Framework](https://github.com/ParisNeo/lollms) - Main Lollms repository

## 🎯 Roadmap

Future toolsets planned:
- [ ] Data Analysis (CSV, JSON, database operations)
- [ ] Web Utilities (HTTP requests, web scraping)
- [ ] Image Processing (resize, convert, analyze)
- [ ] Network Tools (ping, port scanning, network info)
- [ ] Cryptography (hashing, encryption, encoding)
- [ ] Date/Time Utilities (parsing, formatting, calculations)
- [ ] Code Analysis (linting, formatting, metrics)
- [ ] Google Scholar Integration
- [ ] PubMed/MEDLINE Tools
- [ ] Semantic Scholar API Integration

## 💡 Examples

### File Management Example
```python
# The LLM can use these tools naturally:
"List all Python files in the current directory"
# → Calls tool_list_directory(pattern="*.py")

"Read the contents of config.json"
# → Calls tool_read_file(file_path="config.json")
```

### Text Processing Example
```python
"Extract all email addresses from this text"
# → Calls tool_extract_emails(text="...")

"Count how many words are in this document"
# → Calls tool_count_words(text="...")
```

### Math Calculator Example
```python
"What's the average of these numbers: 10, 20, 30, 40?"
# → Calls tool_calculate_mean(numbers=[10, 20, 30, 40])

"Calculate 15% of 200"
# → Calls tool_calculate_percentage(part=15, whole=200)
```

### Bibliography Examples

#### arXiv Search
```python
"Search arXiv for recent papers on transformer architectures"
# → Calls tool_search_arxiv(query="transformer architectures", max_results=10)

"Download the PDF of arXiv paper 2301.00001"
# → Calls tool_download_arxiv_pdf(arxiv_id="2301.00001")
```

#### DOI Resolution
```python
"Get the citation for DOI 10.1038/nature12373"
# → Calls tool_get_citation_by_doi(doi="10.1038/nature12373", style="APA")

"Resolve DOI 10.1109/5.771073 and get full metadata"
# → Calls tool_resolve_doi(doi="10.1109/5.771073")
```

#### Zotero Integration
```python
"Search my local Zotero library for papers about neural networks"
# → Calls tool_zotero_local_search(query="neural networks")

"Add this paper to my Zotero library: DOI 10.1038/nature12373"
# → Calls tool_zotero_remote_add_item(doi="10.1038/nature12373")
```

#### Bibliography Management
```python
"Create a new bibliography for my machine learning research"
# → Calls tool_create_bibliography(name="ml_research")

"Export my bibliography to BibTeX format"
# → Calls tool_export_bibliography(format="bibtex", output_file="references.bib")
```

---

**Made with ❤️ for the Lollms community**

## 📊 Repository Stats

![GitHub repo size](https://img.shields.io/github/repo-size/ParisNeo/lollms_tools_zoo)
![GitHub code size](https://img.shields.io/github/languages/code-size/ParisNeo/lollms_tools_zoo)
![GitHub last commit](https://img.shields.io/github/last-commit/ParisNeo/lollms_tools_zoo)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ParisNeo/lollms_tools_zoo)

### 🌟 Show Your Support

If you find this project useful, please consider giving it a star! It helps others discover these tools and motivates continued development.

[![Star History Chart](https://api.star-history.com/svg?repos=ParisNeo/lollms_tools_zoo&type=Timeline)](https://star-history.com/#ParisNeo/lollms_tools_zoo&Timeline)