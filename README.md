# nanohook

## Webhook server for Nanoleaf lights

This project launches a webhook server that controls a Nanoleaf light array. It's setup to handle a single array, only 2 ops - on & off. Like the plughook container, this is all about allowing my son to control the Nanoleaf using his Elgato Streamdeck.

You pass a few variables into the container, and have the option to set the hook names (ie you can use random strings to secure access). Check out the included example docker-compose file to see the details. Add an action to your buttons that load a web page in the background, drop in the URL for each of your webhooks, and boom, you're set.