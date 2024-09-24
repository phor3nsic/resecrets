# 
![alt text](images/image.png)

###

Resecrets is a powerful tool designed for security researchers and developers to search for sensitive information such as credentials, tokens, and other secrets within directories. Using customizable regular expressions, Resecrets scans files to identify potential leaks and vulnerabilities, helping to enhance the security of your codebase.

### Features

- Customizable regex patterns for targeted searches
- Recursive scanning of directories
- Easy integration into CI/CD pipelines
- Supports multiple file types

### Usage

To use Resecrets, simply specify the directory. The tool will output any matches found, making it easy to locate and address potential security issues.

```sh
resecrets /path/to/scan
```

#### Plus

Try using it with [DownJS](https://github.com/deeplooklabs/downjs)
You can download JS files and use [resecrets](https://github.com/phor3nsic/resecrets)

```sh
cat JS_URLS.txt| downjs && resecrets downjs_output
```

### Install

- via pipx:

```sh
pipx install git+https://github.com/phor3nsic/resecrets
```
- via pip:

```sh
pip install git+https://github.com/phor3nsic/resecrets
```

### In Source:

```python
from resecrets import main as rsecrets

main_dir = rsecrets.MAIN_DIR
pathern = os.path.join(str(Path(main_dir).parent), "config", "regexes.json")
rsecrets.search(pathern, "/PATH_TO_SEARCH/")

```

### Contribute More Regular Expressions!

We welcome contributions to our collection of regular expressions! If you have useful regex patterns to share, please follow these steps:

1. **Open an Issue**: To contribute, simply open an issue on our repository.
2. **Provide Your Regex**: Include your regex in the issue, using the following format:

   - **Single Regex**:
     ```json
     "RESOURCE NAME": "REGEX"
     ```

   - **Multiple Regexes**:
     ```json
     "RESOURCE NAME": [
         "REGEX1",
         "REGEX2"
     ]
     ```

3. **Describe Your Contribution**: Briefly explain what your regex does and why it’s useful.

We’ll review your submission and incorporate it into our project.

Thank you for helping us improve!

### License

This project is licensed under the MIT License.