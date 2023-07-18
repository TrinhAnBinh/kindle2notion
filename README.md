This read me as guide for:
### todo
---
- feat:
[x] add the update page
[x] separate the list into 100 items in a list
[x] get the id of page after creating page, will apply the page after
[ ] update the unitest
[ ] update "updates blocks"
[ ] create the path to notion notes, config parsing

# Kindle Clippings to Notion Pages

This repository provides a solution for processing Kindle clippings and exporting them to Notion pages. It aims to streamline the process of organizing and managing your Kindle highlights and notes within Notion.

## Features

- **Clippings Parser**: Parses the Kindle clippings file and extracts the book information, highlights, and notes.
- **Notion API Integration**: Utilizes the Notion API to create new pages in your Notion workspace and populate them with the extracted Kindle clippings.
- **Customizable Templates**: Allows you to customize the Notion page templates to suit your preferences and organize your clippings in a way that makes sense to you.
- **Tagging and Categorization**: Supports tagging and categorization of clippings for easy search and retrieval within Notion.
- **Efficient and Scalable**: Designed to handle large Kindle clippings files and efficiently process them into Notion pages.

## How It Works

1. **Kindle Clippings File**: Export the Kindle clippings file from your Kindle device or Kindle app.
2. **Configure the Repository**: Set up the repository by providing your Notion integration token and configuring the desired page templates and settings.
3. **Run the Parser**: Execute the parser script, providing the path to the Kindle clippings file as an input.
4. **Notion Page Creation**: The script will process the clippings file, extract the relevant information, and create new pages in your Notion workspace using the provided templates.
5. **Access and Organize Clippings**: Open Notion and navigate to the designated workspace to access and organize your Kindle highlights and notes.

## Getting Started

To get started with this repository, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.

   ```bash
   git clone https://github.com/TrinhAnBinh/kindle2notion.git
   ```

2. **Install Dependencies**: Install the necessary dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Repository**: Open the repository and modify the configuration file (`config.py`) with your Notion integration token and other desired settings.

4. **Set up Notion Templates**: Create the desired Notion page templates in your workspace and configure their properties and layout to match your requirements.

5. **Prepare Notion API**: Prepare, get the key, template for Notion pages

6. **Run the Parser**: Execute the parser script, providing the path to your Kindle clippings file as an argument.

   ```bash
   python parser.py --clippings-file /path/to/your/clippings.txt
   ```

7. **Access Your Clippings**: Open Notion and navigate to the designated workspace to access and organize your Kindle clippings in the newly created pages.


## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to add new features, please feel free to open an issue or submit a pull request.

## License

This repository is licensed under the [MIT License](LICENSE).