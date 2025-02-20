# Como Rodar o Projeto


## **1️⃣ Criar um Ambiente Virtual**
Para garantir que todas as dependências sejam instaladas corretamente sem interferir em outras instalações do seu sistema, crie um ambiente virtual:

```bash
python3 -m venv venv
```

## **2️⃣ Ativar o Ambiente Virtual**
Agora, ative o ambiente virtual:

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

Se o nome do prompt mudar para `(venv)`, significa que o ambiente virtual foi ativado com sucesso. ✅

## **3️⃣ Instalar as Dependências**
Após ativar o ambiente virtual, instale todas as dependências necessárias para rodar o projeto:

```bash
pip install -r requirements.txt
```

Isso instalará todas as bibliotecas listadas no arquivo `requirements.txt`.

## **4️⃣ Navegar até o Diretório Correto**
Agora, vá até a pasta onde o arquivo `0_Apresentacao.py` está localizado:

```bash
cd pages  # Se necessário, ajuste o caminho para onde o arquivo está
```

## **5️⃣ Rodar o Projeto com o Streamlit**
Finalmente, execute o projeto com o comando:

```bash
streamlit run 0_Apresentacao.py
```

Isso abrirá o projeto no seu navegador padrão, e você poderá interagir com a aplicação. 🎉

## **6️⃣ Desativar o Ambiente Virtual (Opcional)**
Quando terminar de usar o projeto, você pode desativar o ambiente virtual com:

```bash
deactivate
```



