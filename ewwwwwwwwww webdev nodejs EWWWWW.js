let fs = require("fs");
let typo = require("typo-js")
let unaetherer = new typo("en_US");
let https = require("https");

function get_config() {
    return JSON.parse(fs.readFileSync("config.json"));
}

let kde_dragons = require("./kde-dragons/catalogue.json")

const { exec } = require("child_process");
let discord = require("discord.js");
let secrets = require("./secrets.json");
let friend_codes = require("./friend-codes.json");
const { AttachmentBuilder } = require("discord.js");
let config = get_config();
let client = new discord.Client({
    intents:
        discord.GatewayIntentBits.GuildMessages |
        discord.GatewayIntentBits.GuildMembers |
        discord.GatewayIntentBits.GuildMessageReactions |
        discord.GatewayIntentBits.Guilds |
        discord.GatewayIntentBits.MessageContent
});

let selected_messages = {};
let srs_channels = [];

let aetherLetters = ["π","§","ů","ö","🗣️","ǚ","ǘ","ǜ","ů̈́"];

function ping_manager() {
    let date = new Date();
    let hour = date.getHours();
    let minute = date.getMinutes();
    let second = date.getSeconds();
    let people_to_ping = [];
    if (hour == 17 && minute == 0 && second == 0) {
        people_to_ping.push("568783323933966336");
    }
    if (hour == 6 && minute == 0 && second == 0) {
        people_to_ping.push("708030466502164572");
    }
    if (people_to_ping.length == 0) return;
    client.channels.fetch("1232421214979362850").then((c) => {
        for (let person of people_to_ping) {
            c.send("<@" + person + ">");
        }
    })
}

function wait(sec) {
    return new Promise(resolve => {
        setTimeout(resolve, sec * 1000);
    });
}

function get_catboy(server_id) {
    let files = fs.readdirSync("catboys");
    let catboy = "catboys/" + files[Math.floor(Math.random() * files.length)];
    if (server_id == "1203300325721772132" && catboy == "catboys/11.png") catboy = "catboys/10.png";
    return catboy;
}

function bully_aether(server_id) {
    return { content: ":3", files: [ get_catboy(server_id) ] };
}

client.on("ready", function() {
    /*let func;
    let sum = 33;
    let count = 3;
    let last = 1395792;*/
    client.user.setActivity("aether stay away from me", { type: discord.ActivityType.Custom });
    /*setInterval(func = function() {
        https.get("https://eci.ec.europa.eu/045/public/api/report/progression", res => {
            let data = "";
            res.on("data", chunk => data += chunk);
            res.on("end", () => {
                let num = JSON.parse(data).signatureCount;
                let percent = Math.floor(num / 1400000 * 100000) / 1000;
                let diff = num - last;
                let remain = 1400000 - num;
                sum += diff;
                count++;
                let avg = sum / count;
                let eta = (remain / avg) * 5;
                let eta_hour = Math.floor(eta / 60);
                let eta_min = Math.floor(eta) % 60;
                let eta_sec = Math.floor(eta % 60);
                let msg = "SKG signatures: " + num + "/1400000 (" + percent + "%)\nRemaining: " + remain + " (" + (eta_hour > 0 ? eta_hour + "h" : "") + eta_min + "m" + eta_sec + "s)\n-# " + diff + " signatures gained in the past 5 minutes";
                client.guilds.fetch("1232421214069325964").then(g => g.channels.fetch("1232421214979362850").then(c => c.send(msg)));
                last = num;
            });
        });
    }, 5*60*1000);*/
    //func();
});

client.on("interactionCreate", async function(interaction) {
    if (interaction.type == discord.InteractionType.ApplicationCommand) {
        if (interaction.commandName == "updatecfg") {
            config = get_config();
            interaction.reply({ content: "config updated", ephemeral: true });
        }
        if (interaction.commandName == "react") {
            if (!selected_messages[interaction.user.id]) {
                interaction.reply({ content: "you havent selected a message vro❤️", ephemeral: true });
            }
            let ruleID = interaction.options.getString("id");
            let msgID = selected_messages[interaction.user.id];
            let msg = await interaction.channel.messages.fetch(msgID)
            if (react_with(msg, [ruleID])) interaction.reply({ content: "okkiii reacting this mf rn", ephemeral: true });
            else interaction.reply({ content: "wtf is this reaction vro❤️", ephemeral: true });
        }
        if (interaction.commandName == "listreact") {
            interaction.reply({ content: ("- " + get_valid_reactions(interaction.guild.id).join("\n- ")), ephemeral: true });
        }
        if (interaction.commandName == "opensource") {
            interaction.reply({ content: ":3", files: [ "./index.js", "./config.json" ] })
        }
        if (interaction.commandName == "neofetch") {
            console.log("test");
            let promise = interaction.deferReply();
            let child = exec("neofetch --config none | sed 's/\\x1B\\[[0-9;]*m//g' | ./processansi");
            let neofetch = "";
            child.stdout.on("data", function(chunk) {
                neofetch += chunk.toString();
            });
            child.on('exit', async function() {
                await promise;
                interaction.editReply({ content: "```\n" + neofetch.split("`").join("'") + "\n```" });
            });
        }
        if (interaction.commandName == "cataeth") {
            interaction.reply({ content: "👍", ephemeral: true });
            console.log("/cataeth triggered by " + interaction.user.globalName);
            if (selected_messages[interaction.user.id]) {
                let msg = await interaction.channel.messages.fetch(selected_messages[interaction.user.id]);
                msg.reply(bully_aether(interaction.guild.id));
            }
            else interaction.channel.send(bully_aether(interaction.guild.id));
            selected_messages[interaction.user.id] = undefined;
        }
        if (interaction.commandName == "seelct messag") {
            interaction.reply({ content: "👍", ephemeral: true });
            selected_messages[interaction.user.id] = interaction.targetMessage.id;
        }
        if (interaction.commandName == "switchfriend") {
            if (interaction.options.getSubcommand() == "register") {
                friend_codes[interaction.user.id] = interaction.options.getString("code");
                fs.writeFileSync("friend-codes.json", JSON.stringify(friend_codes));
                interaction.reply("done");
            }
            if (interaction.options.getSubcommand() == "get") {
                let user = interaction.options.getUser("user");
                let code = friend_codes[user.id];
                if (code) interaction.reply("**" + user.displayName + "**: `" + code + "`");
                else interaction.reply("no code yet vro,,,.,..,,......");
            }
        }
        if (interaction.commandName == "talk") {
            console.log((interaction.user.displayName ?? interaction.user.username) + " used /talk");
            interaction.reply({ content: "👍", ephemeral: true });
            let content = interaction.options.getString("msg");
            console.log(content);
            if (selected_messages[interaction.user.id]) {
                let msg = await interaction.channel.messages.fetch(selected_messages[interaction.user.id]);
                msg.reply(content);
            }
            else interaction.channel.send(content);
            selected_messages[interaction.user.id] = undefined;
        }
        if (interaction.commandName == "spoon") {
            await interaction.deferReply();
            let rand = Math.random();
            let file = "spoon.png";
            if      (rand < 0.1) file = "actualspoon.png";
            else if (rand < 0.2) file = "whatthefuckspoon.gif";
            interaction.editReply({ content: "spoon", files: [ file ] });
        }
        if (interaction.commandName == "grandpa") {
            await interaction.deferReply();
            interaction.editReply({ content: "grandoa 💞", files: [ "grandpa.png" ]});
        }
        if (interaction.commandName == "getou") {
            await interaction.deferReply();
            let child = exec("./GETOU.sh");
            await wait(1);
            interaction.editReply({ content: "GETOU🗣️🗣️🗣️", files: [ "GETOU.mp3" ] });
        }
        if (interaction.commandName == "aetherificator") {
            let message = interaction.options.getString("msg");
            let aetherified = "";
            for (let i = 0; i < message.length; i++) {
                let code = message.charCodeAt(i) - 0x10;
                if (code == 0x10) aetherified += " ";
                else if (code < 0x20) aetherified += aetherLetters[Math.floor(Math.random() * aetherLetters.length)];
                else aetherified += String.fromCharCode(code);
            }
            interaction.reply({ content: aetherified });
        }
        if (interaction.commandName == "unaetherificator") {
            await interaction.deferReply();
            let message = interaction.options.getString("msg");
            let words = message.trim().replaceAll(" +", " ").split(" ");
            for (let i = 0; i < words.length; i++) {
                if (unaetherer.check(words[i])) continue;
                words[i] = unaetherer.suggest(words[i])[0];
            }
            words = words.join(" ").trim();
            if (words == "") words = "failed to unaether, shits too aethered :<";
            interaction.editReply({ content: words });
        }
        if (interaction.commandName == "serious") {
            if (!srs_channels.includes(interaction.channel.id)) srs_channels.push(interaction.channel.id);
            interaction.reply("channel has been srs'd");
        }
        if (interaction.commandName == "joke") {
            if (srs_channels.includes(interaction.channel.id)) srs_channels.splice(srs_channels.indexOf(interaction.channel.id), 1);
            interaction.reply("channel has been j'd");
        }
        if (interaction.commandName == "cat") {
            await interaction.deferReply();
            await fetch("https://cataas.com/cat?json=1").then(async (res) => {
                let json = await res.json();
                await interaction.editReply(`heres a random [ktiiy](${json.url}) image :3`);
            }).catch(async (err) => interaction.editReply("cats are too eepy so the api is down :<"));
        }
        if (interaction.commandName == "fox") {
            // FluffyKn1ght was here *yip* :3c
            //console.log(`${interaction.id} ${interaction.isRepliable()}`)
            //console.log("deferring reply")
            await interaction.deferReply()
            //console.log("deferred reply")

            await fetch("https://randomfox.ca/floof/")
                .then(async (response) => {
                    try {
                        const img_info = await response.json()

                        const dlResp = await fetch(await img_info["image"])

                        const arrayBuf = await dlResp.arrayBuffer()
                        const buffer = Buffer.from(arrayBuf)

                        const attachment = new AttachmentBuilder(buffer, { "name": "fxoe.jpg" })
                        await interaction.editReply({ content: `link to fxoe image: <${img_info["link"]}> :3`, files: [attachment]} );
                    } catch (error) {
                        console.error(`error while downloading /fox pic: ${error}`)
                        await interaction.followUp({
                            content: `could not get fxoe :<\n-# \`${error}\``
                        })
                    }
                })
                .catch(async (error) => {
                    console.error(`error while getting /fox pic: ${error}`)
                    await interaction.followUp({
                        content: `the fxoe™®© service™®© is currently too eepy plz check back later -w-\n-# \`${error}\``
                    })
                })
            }
        if (interaction.commandName == "kde_dragon") {
            await interaction.deferReply()

            targetTag = interaction.options.getString("dragon") ?? ["konqi", "katie", "kori", "other"][Math.floor(Math.random() * 4)]

            validOptions = []
            kde_dragons.forEach((value, _idx, _arr) => {
                if (value["tags"].includes(targetTag)) {
                    validOptions.push(value)
                }
            })

            option = validOptions[Math.floor(Math.random() * validOptions.length)]

            pictureInfo = "kde dragon"
            if (interaction.options.getString("dragon") && interaction.options.getString("dragon") != "other") {
                pictureInfo = interaction.options.getString("dragon")
            }

            imageAttach = new AttachmentBuilder(`./kde-dragons/${option["file"]}`)

            await interaction.editReply(
                {
                    content: `here is your ${pictureInfo} picture! :3\n-# please visit [this page](<https://community.kde.org/Promo/Material/Mascots>) for licensing/credit/other info\n-# a full quality version of this image is available [here](<${option["url"]}>)`,
                    files: [imageAttach]
                }
            )
        }
    }
});

function get_valid_reactions(id) {
    if (!id) return config.rules;
    let valid = [];
    for (let [rule_id, rule] of Object.entries(config.rules)) {
        if (!rule.whitelist || rule.whitelist.includes(id)) valid.push(rule_id);
    }
    return valid;
}

async function handle_msg(msg1, msg2) {
    let msg = msg2 ?? msg1;
    let funny = config.funnies[msg.content.toLowerCase()];
    if (funny) msg.channel.send(funny);
    if (!msg.member) return;
    await msg.guild.members.fetch(msg.member.id);
    for (let [role, channel] of Object.entries(config.horny)) {
        if (msg.member.roles.cache.has(role) && (await msg.guild.channels.fetch(channel)) && !channel.includes(msg.channel.id)) {
            msg.delete();
            return;
        }
    }
    if (config.channel_blacklist.includes(msg.channel.id)) return;
    if (srs_channels.includes(msg.channel.id)) return;
    if (config.fire_level == 1 && msg.channel.id == "1203431724550455356") msg.react("🔥");
    if (config.fire_level == 2 && msg.channel.id == "1203431724550455356") msg.react("💥");
    let content = msg.content.toLowerCase();
    let reaction_ids = [];
    for (let rule of get_valid_reactions(msg1.guild.id)) {
        let should_react = false;
        for (let keyword of config.rules[rule].keywords) {
            if (content.match(new RegExp(keyword))) {
                should_react = true;
                break;
            }
        }
        if (!should_react) continue;
        reaction_ids.push(rule);
    }
    react_with(msg, reaction_ids);
}

let geolayouts = {};

client.on("messageCreate", (msg) => {
    handle_msg(msg);
    if (msg.author.bot) return;
    if (geolayouts[msg.channel.id]) {
        geolayouts[msg.channel.id] = false;
        if (msg.content.toLowerCase() == "out") {
            msg.react("<:goodjob:1190754284854325381>");
        }
        else {
            let reply = config.geolayout[""];
            for (let [keyword, reply_msg] of Object.entries(config.geolayout)) {
                if (keyword == "") continue;
                if (msg.content.toLowerCase().match(new RegExp(keyword))) {
                    reply = reply_msg;
                    break;
                }
            }
            msg.reply(reply);
        }
    }
    if (msg.content.toLowerCase() == "geo") {
        msg.reply("lay".split("").map((char, index) => msg.content[index] == msg.content[index].toUpperCase() ? char.toUpperCase() : char.toLowerCase()).join(""));
        geolayouts[msg.channel.id] = true;
    }
});
client.on("messageUpdate", handle_msg);

// fuck you dan
client.on("messageReactionAdd", async function(reaction, user) {
    for (let [role, channel] of Object.entries(config.horny)) {
        if (reaction.message.member.roles.cache.has(role) && (await reaction.message.guild.channels.fetch(channel)) && reaction.message.channel.id != channel) reaction.users.remove(user);
    }
    if (user.id != "898296720226668554") return;
    if (reaction.emoji.name == "⭐") return;
    if (reaction.count > 1) return;
    reaction.message.channel.send("fuck you dan");
    let dan = await client.users.fetch(user.id);
    reaction.users.remove(user);
});

client.on("ready", function() {
    console.log("ready");
    //setInterval(ping_manager, 1000);
});

client.on("guildMemberUpdate", async function(oldMember, newMember) {
    let removed = oldMember.roles.cache.filter(role => !newMember.roles.cache.has(role.id));
    let logs = await newMember.guild.fetchAuditLogs({ limit: 1, type: 25 }).catch(() => null);
    let log = logs.entries.first();
    if (log && log.executor.id == newMember.id) {
        for (role of removed.values()) {
            if (Object.keys(config.horny).includes(role.id)) {
                newMember.roles.add(role);
            }
        }
    }
});

let rest = new discord.REST({ version: '10' }).setToken(secrets.token)
rest.put(
	discord.Routes.applicationCommands(config["app_id"]),
	{ body: [
		new discord.SlashCommandBuilder()
            .setName("updatecfg")
            .setDescription("update the config")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("react")
            .setDescription("manually triggers a reaction")
            .addStringOption(new discord.SlashCommandStringOption()
                .setName("id")
                .setDescription("the reaction id")
                .setRequired(true)
            )
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("listreact")
            .setDescription("lists all reaction ids")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("opensource")
            .setDescription("sends the fuckin source code lmfao")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("neofetch")
            .setDescription("runs neofetch on the server")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("cataeth")
            .setDescription("skibidi toilet")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("switchfriend")
            .setDescription("the switch friend list lma")
            .addSubcommand(new discord.SlashCommandSubcommandBuilder()
                .setName("register")
                .setDescription("regitser a friend code 🙏🙏🙏")
                .addStringOption(new discord.SlashCommandStringOption()
                    .setName("code")
                    .setDescription("the code xro ❤️")
                    .setRequired(true)
                )
            )
            .addSubcommand(new discord.SlashCommandSubcommandBuilder()
                .setName("get")
                .setDescription("gets the thing")
                .addUserOption(new discord.SlashCommandUserOption()
                    .setName("user")
                    .setDescription("someone idk")
                    .setRequired(true)
                )
            )
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("talk")
            .setDescription("fjdskfsjdfkj")
            .addStringOption(new discord.SlashCommandStringOption()
                .setName("msg")
                .setDescription("jdkfskfd")
                .setRequired(true)
            )
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("spoon")
            .setDescription("the spoon")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("grandpa")
            .setDescription("actual fossil")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("getou")
            .setDescription("GETOU🗣️🗣️🗣️")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("aetherificator")
            .setDescription("instant aethering")
            .addStringOption(new discord.SlashCommandStringOption()
                .setName("msg")
                .setDescription("text to aetherify")
                .setRequired(true)
            )
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("unaetherificator")
            .setDescription("instant unaethering")
            .addStringOption(new discord.SlashCommandStringOption()
                .setName("msg")
                .setDescription("text to unaetherify")
                .setRequired(true)
            )
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("serious")
            .setDescription("turns off the thing in this channel")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("joke")
            .setDescription("turns on the thing in this channel")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("fox")
            .setDescription("sends a random fxoe picture :3")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("cat")
            .setDescription("sends a random ktiiy picture :3")
        .toJSON(),
        new discord.SlashCommandBuilder()
            .setName("kde_dragon")
            .setDescription("sends a random kde dragon picture :3")
            .addStringOption(new discord.SlashCommandStringOption()
                .setName("dragon")
                .setDescription("the dragon to send a picture of! (optional, random otherwise)")
                .setRequired(false)
                .addChoices([
                    { name: "Konqi", value: "konqi" },
                    { name: "Katie", value: "katie" },
                    { name: "Kori", value: "kori" },
                    { name: "Other", value: "other" },
                ])
        )
        .toJSON(),
        new discord.ContextMenuCommandBuilder()
            .setName("seelct messag")
            .setType(discord.ApplicationCommandType.Message)
        .toJSON(),
	]},
);

client.login(secrets.token);

function react_with(msg, reaction_ids) {
    if (msg.author.id == "568783323933966336" && reaction_ids.includes("cat")) {
        msg.reply(bully_aether(msg.guild.id));
    }
    let pending_reactions = [];
    for (let rule of reaction_ids) {
        if (!config.rules[rule]) return false;
        for (let emoji of config.rules[rule].reactions) {
            pending_reactions.push(emoji);
        }
    }
    let reactions_left = [];
    let failed = false;
    for (let reaction of pending_reactions) {
        reactions_left.push(reaction);
    }
    while (reactions_left.length > 0) {
        let index = Math.floor(Math.random() * reactions_left.length);
        msg.react(reactions_left[index]).catch(function(err) {
            if (failed) return;
            failed = true;
        });
        reactions_left.splice(index, 1);
    }
    return true;
}

