# Google Fit Home Assistant Custom Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

This integration interfaces with the [Google Fit REST API][rest-api] to provide Google Fit
data within Home Assistant.

![Example](/res/example.png)

**This integration will set up the following platforms.**

Platform | Name |Description
-- | -- | --
`sensor` | `active_minutes_daily` | Active Minutes. Reset daily.
`sensor` | `calories_burnt_daily` | Calories burnt (kcal). Reset daily.
`sensor` | `distance_travelled_daily` | Distance (metres) travelled. Reset daily.
`sensor` | `heart_points_daily` | Heart Points earned. Reset daily.
`sensor` | `height` | Height (metres).
`sensor` | `weight` | Weight (kilograms).
`sensor` | `steps` | Number of steps taken. Reset daily.

## Prerequisites

### Authentication Configuration

I will not try to duplicate what has already been documented countless times before as it will no doubt become out
of date.

Instead, follow the instruction in the Official home Assistant Docs for [Google Mail][google-mail] under the
"Generate Client ID and Client Secret" section, replacing instructions for 'Gmail API' with 'Fit API'.

## Installation

### HACS (Recommend)

#### Once available

1. Go to Integrations
1. Click Explore & Download Repositories
1. Find the integration as `Google Fit`
1. Click install.
1. Restart Home Assistant.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Google Fit"

#### Manual

1. Go to Integrations
1. Click on the 3 dots in the top right
1. Click Custom Repositories
1. Add this repository as an integration (https://github.com/YorkshireIoT/ha-google-fit)
1. Search for `Google Fit` and install
1. Restart Home Assistant.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Google Fit"

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `google_fit`.
1. Download _all_ the files from the `custom_components/google_fit/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Google Fit"

## Configuration is done in the UI

Just go to Integrations->Add Integration and follow the steps.
If you have set the app you created in the Credentials configuration to publish
(which you should've done to avoid re-authentication problems) then you
will probably see a warning step asking if you want to proceed.

You can hit "Advanced", then "Proceed" as *you* are the 'developer' of the app,
as you created the app and credentials in your own account.

### Configuration Example Screenshots

![Add Integration](/res/add.png)
![Add Credentials](/res/add_credentials.png)
![Choose Google Account](/res/choose_account.png)
![Unverified Warning](/res/warning.png)
![Access Request with Scopes](/res/wants_access.png)
![Link Account](/res/link_account.png)
![Finished](/res/success.png)


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[buymecoffee]: https://www.buymeacoffee.com/yorkshireiot
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/YorkshireIoT/ha-google-fit.svg?style=for-the-badge
[commits]: https://github.com/YorkshireIoT/ha-google-fit/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/YorkshireIoT/ha-google-fit.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%20%40YorkshireIoT-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/YorkshireIoT/ha-google-fit.svg?style=for-the-badge
[releases]: https://github.com/YorkshireIoT/ha-google-fit/releases
[rest-api]: https://developers.google.com/fit/rest
[google-mail]: https://next.home-assistant.io/integrations/google_mail/