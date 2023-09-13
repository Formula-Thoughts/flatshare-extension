# Flatshare Extension

A browser extension that helps organise your flatshare search

This project uses <a href="https://www.flaticon.com/free-icons/partnership" title="partnership icons">Partnership icons created by Flat Icons - Flaticon</a>

# Back End
- Install packages
  - `pip install -r requirements.txt && pip install -r requirements-test.txt`
- Deploy
  - must have a local samconfig.toml file which contains nessecary secrets, optionally when doing a sam deploy, add the -g flag to do a guided deployment https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html
  - `clean_build_winblows.cmd` (for windows) `clean_build.sh` (for unix)
  - `cd ..\..\..`
  - `sam deploy`
- Run tests
  - `python -m unittest`

# Front End
- Install packages
  - `npm install`
- Build extension
  - `npm run build`
- Open extension in browser
  ![nativate to browsers extension page](.readme_files/extensions-location.png)

- Switch into developer mode
  ![developer mode switch](.readme_files/developer-mode.png)

  ![developer mode switch](.readme_files/developer-mode-on.png)

- Load unpacked extension into Chrome or Brave

  - Click Load unpacked button
  - Select the dist directory

    ![dist directory selected](.readme_files/load-dist-dir.png)
