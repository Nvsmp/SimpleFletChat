import flet as ft

def main(pagina):
  texto_inicial = ft.Text("Raul's Zap")
  nome_usuario = ft.TextField()
  chat = ft.Column()

  def enviar_mensagem_tunel(mensagem):
    if mensagem['texto'] != "":
      #adicionar mensagem no chat
      chat.controls.append(
          ft.Text(f"Sr.{mensagem['usuario']}: {mensagem['texto']}"))
      #limpar o campo mensagem
      campo_mensagem.value = ""
      pagina.update()

  pagina.pubsub.subscribe(enviar_mensagem_tunel)

  def enviar_mensagem(evento):
    pagina.pubsub.send_all({
        "texto": campo_mensagem.value,
        "usuario": nome_usuario.value
    })
    campo_mensagem.value = ""
    pagina.update()

  campo_mensagem = ft.TextField(label="Digite uma mensagem")
  botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

  def entrar_popup(evento):
    pagina.add(chat)
    popup.open = False
    pagina.remove(botao_iniciar)
    pagina.remove(texto_inicial)
    pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))
    pagina.update()

  popup = ft.AlertDialog(
      open=False,
      modal=True,
      title=ft.Text("Bem vindo Sr..."),
      content=nome_usuario,
      actions=[ft.ElevatedButton("ENTRAR", on_click=entrar_popup)],
  )

  def entrar_chat(evento):
    pagina.dialog = popup
    popup.open = True
    pagina.update()

  botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)
  pagina.add(texto_inicial)
  pagina.add(botao_iniciar)


ft.app(target=main, view=ft.WEB_BROWSER)  #