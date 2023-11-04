import vk_api, random, time
from vk_api.longpoll import VkLongPoll, VkEventType
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
vk = vk_api.VkApi(token='TOKEN')
admin_webhook_url = 'https://discord.com/api/webhooks/URL'
admin_webhook = DiscordWebhook(url=admin_webhook_url, rate_limit_retry=True, username="VK-SEARCHES")
def all():
    try:
        longpoll = VkLongPoll(vk)
        list = [303,293,300,260,301,279,302,287,220,263]
        repeated_msgs = []
        t = 0

        while True:
            try:

                for event in longpoll.listen():
                    try:
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.chat_id in list:

                                text = event.text.lower()
                                split = text.split()
                                if 'ищу' in split or 'куплю' in split or 'wtb' in split or 'buy' in split or 'ищу/куплю' in split or 'ищу/куплю' in split or '#ищу' in split:
                                    if t > len(list):
                                        try:
                                            repeated_msgs.remove(text)
                                            t = 0
                                        except:
                                            pass
                                    u_id = event.user_id
                                    msg_id = event.message_id
                                    msg = vk.method("messages.getById",{'message_ids':msg_id})
                                    print(msg)
                                    print(u_id)
                                    group_f = vk.method("messages.getChat", {'chat_id': event.chat_id})
                                    print(group_f)
                                    group = (group_f['title'])
                                    print(group)
                                    name = vk.method("users.get",{'user_ids':u_id})
                                    first_name = (name[-1]['first_name'])
                                    last_name = (name[-1]['last_name'])
                                    print(first_name+' '+last_name)

                                    try:
                                        img = (msg['items'][-1]['attachments'][-1]['photo']['sizes'][-1]['url'])
                                    except:
                                        img = 'https://upload.wikimedia.org/wikipedia/commons/2/21/VK.com-logo.svg'
                                    print(text)


                                    embed_success = DiscordEmbed(title=f'{first_name} {last_name}',url=f'https://vk.com/id{u_id}',description=text, color='ffffff')
                                    embed_success.set_image(url=img)
                                    embed_success.add_embed_field(name='Message From:',value=group)
                                    embed_success.set_footer(text='Developed by Misha Ivakhov\n' + str(datetime.datetime.now()),icon_url='url')
                                    admin_webhook.remove_embeds()
                                    admin_webhook.add_embed(embed_success)

                                    if text not in repeated_msgs:
                                        repeated_msgs.append(text)
                                        admin_webhook.execute()

                                        a = 0
                                        b = 0
                                        while a < len(split):
                                            try:
                                                print(split[a])
                                                file = open(f'{split[a]}.txt', 'r')
                                                a = a + 1
                                                read = file.read()
                                                file.close()
                                                spl_read = read.split('\n')
                                                try:
                                                    spl_read.remove('\n')
                                                except:
                                                    pass
                                                print(len(spl_read))

                                                while b < len(spl_read):
                                                    content = f"<@{spl_read[b]}>"
                                                    webhook_text = DiscordWebhook(url=admin_webhook_url, content=content)
                                                    if content!='<@>':
                                                        execute = webhook_text.execute()
                                                    b = b + 1

                                            except Exception as ex:
                                                a = a + 1
                                                print(ex)



                    except Exception as ex:
                        if str(ex) =="'Event' object has no attribute 'chat_id'":
                            print('DIRECT MESSAGE DETECTED')
                        print(ex)
            except:
                print(str(datetime.datetime.now()) + 'CONNECTION LOST')
    except:
        print(str(datetime.datetime.now())+'CONNECTION LOST')
        all()
all()