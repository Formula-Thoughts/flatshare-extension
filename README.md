<style>
  .image-wrapper {
    display: inline-block; /* Ensures the span wraps around the image */
  
    max-width: 300px; /* Maximum width for the image */
    max-height: 300px; /* Maximum height for the image */
  }
  .image-container {
    display: flex;
    align-items: center;
  }
  .image-container span {
    margin: 0 10px; /* Adjust spacing between images */
  }

</style>

# Flatini

Helps organise your flat share search

<details>
  <summary>Frontend</summary>
  
  Front end section
</details>

<details>
  <summary>Backend</summary>

Located under the [backend](./backend/) directory of the project. A python based serverless application handling backend tasks including authentication, api, and data.

- live at https://gbjrcfuc7b.execute-api.eu-west-2.amazonaws.com/groups/5130831f-f57f-42e6-87fc-894ba74eea6e
- Install packages
  - `pip install -r requirements.txt && pip install -r requirements-test.txt`
- Deploy
  - must have a local samconfig.toml file which contains nessecary secrets, optionally when doing a sam deploy, add the -g flag to do a guided deployment https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html
  - `clean_build_winblows.cmd` (for windows) `clean_build.sh` (for unix)
  - `sam deploy`
- Run tests - `python -m unittest`

</details>

<details>
  <summary>Browser Extension</summary>

Located under the [client](./client/) directory of the project. A JS based chrome extension.

- In a terminal, change folder to the client folder under the root of the project
- Install packages
  - `npm install`
- Build extension
  - `npm run build`
- Open extension in browser

  <span class="image-wrapper">![nativate to browsers extension page](.readme_files/extensions-location.png)</span>

- Switch into developer mode

  <div class="image-container">
    <img width="300" src=".readme_files/developer-mode.png" alt="developer mode switch off">
    <span>TO</span>
    <img width="300" src=".readme_files/developer-mode-on.png" alt="developer mode switch on">
  </div>

- Load unpacked extension into Chrome [Brave unfortunately doesn't support side panels at this time]

  - Click Load unpacked button
  - Select the dist directory

    <span class="image-wrapper">![dist directory selected](.readme_files/load-dist-dir.png)</span>

  - You will now see Flatini loaded into your extension.

    <span class="image-wrapper">![flatini loaded](.readme_files/flatini-extension-loaded.png)</span>

- Open the side panel and select Flatini extension

  <span class="image-wrapper">![flatini side panel](.readme_files/flatini-side-panel.png)</span>

</details>

This project uses <a href="https://www.flaticon.com/free-icons/partnership" title="partnership icons">Partnership icons created by Flat Icons - Flaticon</a>
