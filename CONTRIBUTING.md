# Contribution guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Github is used for everything

Github is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `main`.
2. If you've changed something, update the documentation.
3. Make sure your code lints (using `scripts/lint`).
4. Test you contribution.
5. Issue that pull request!

## Visual Studio Code is the recommended IDE

This repository is built around the developer working in VS Code. It features a devcontainer to
ensure a consistent development environment for anyone working on the repository.

This devcontainer makes use of a Docker container, which means you will need Docker
running on your machine as well.

Of course, you're free to develop in any environment you want but the standards at pull request
are enforced around development in VS Code.

### Getting Started

Follow the official Home Assistant instructions for developers: [Set up Development
Environment](https://developers.home-assistant.io/docs/development_environment/)

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](../../issues)

GitHub issues are used to track public bugs.
Report a bug by [opening a new issue](../../issues/new/choose); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Use a Consistent Coding Style

Use [black](https://github.com/ambv/black) to make sure the code follows the style.

## Test your code modification

This custom component is based on [integration_blueprint template](https://github.com/ludeeus/integration_blueprint).

It comes with development environment in a container, easy to launch
if you use Visual Studio Code. With this container you will have a stand alone
Home Assistant instance running and already configured with the included
[`configuration.yaml`](./configuration.yaml)
file.

### Debugging

Debugging is done using the [Remote Python Debugger](https://www.home-assistant.io/integrations/debugpy/).

Enable it by commenting on the relevant lines in
[`configuration.yaml`](./configuration.yaml).

With this configuration Home Assistant will pause on start up, waiting for the debugger to attach.
You can do this by pressing F5 or going to the 'Run and Debug' tab on the left.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
