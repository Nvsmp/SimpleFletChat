import flet as ft
def main(pagina):
  pagina.scroll = ft.ScrollMode.ALWAYS
  texto_inicial = ft.Text("Raul's Zap")
  nome_usuario = ft.TextField()
  chat = ft.Column()
  
  #FUNCAO DO PUBSUB
  def enviar_mensagem_tunel(mensagem):
    #TESTAR SE O TEXTO NAO ESTA VAZIO
    if mensagem['texto'] != "":
      #TESTAR SE E MENSAGEM NORMAL OU A DE BOAS VINDAS 
      if mensagem["tipo"] == "msg":
        #adicionar mensagem no chat
        chat.controls.append(
        ft.Text(f"Sr.{mensagem['usuario']}: {mensagem['texto']}"))
        #limpar o campo mensagem
        campo_mensagem.value = ""
        campo_mensagem.focus()
        pagina.update()
      else:
        #adicionar mensagem no chat
        chat.controls.append(
        ft.Text(f"Sr.{mensagem['usuario']} acaba de se juntar a conversa !",size=12,italic=True,color=ft.colors.DEEP_ORANGE_500))
        #limpar o campo mensagem
        campo_mensagem.value = ""
        campo_mensagem.focus()
        pagina.update()
    else:
      campo_mensagem.focus()
      pagina.update()

  #EVENTO DO CLIQUE DE ENVIAR MENSAGEM
  def enviar_mensagem(evento):
    pagina.pubsub.send_all({
        "texto": campo_mensagem.value,
        "usuario": nome_usuario.value,
        "tipo":"msg"
    })
    campo_mensagem.value = ""
    pagina.update()

  campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
  botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

  #EVENTO CLIQUE POPUP DE ACESSO
  def entrar_popup(evento):
    if nome_usuario.value != "":
      pagina.pubsub.subscribe(enviar_mensagem_tunel)
      pagina.add(chat)
      popup.open = False
      pagina.remove(botao_iniciar)
      pagina.remove(texto_inicial)
      pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))
      pagina.pubsub.send_all({"usuario":nome_usuario.value,"texto":"ENTROU NO CHAT!","tipo":"join"})
      campo_mensagem.focus()
      pagina.update()
    else:
      campo_mensagem.focus()
      pagina.update()

  #POPUP DE ACESSO
  popup = ft.AlertDialog(
      open=False,
      modal=True,
      title=ft.Text("Bem vindo Sr..."),
      content=nome_usuario,
      actions=[ft.ElevatedButton("ENTRAR", on_click=entrar_popup)],
  )

  #EVENTO CLIQUE TELA INICIAL
  def entrar_chat(evento):
    pagina.dialog = popup
    popup.open = True
    pagina.update()

  #LAYOUT DE INICIO DA FUNCAO MAIN
  botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)
  pagina.add(texto_inicial)
  pagina.add(botao_iniciar)
ft.app(target=main, view=ft.WEB_BROWSER)  #