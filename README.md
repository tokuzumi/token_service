Token Service AiVoice
1. Visão Geral
O Token Service AiVoice é uma API HTTP, desenvolvida em Python com FastAPI, responsável por gerar tokens de acesso JWT (JSON Web Token) compatíveis com o servidor LiveKit.

Seu objetivo é centralizar e padronizar a autenticação de usuários para todas as soluções da AiVoice que utilizam a infraestrutura de comunicação em tempo real, garantindo um processo de autorização seguro e unificado.

2. Uso da API (Para Desenvolvedores Frontend)
Esta seção detalha como as aplicações cliente devem consumir a API para obter um token de acesso.

Endpoint
URL: https://token.aivoice.com.br

Método: POST

Header: Content-Type: application/json

Requisição (Request)
O corpo da requisição deve ser um objeto JSON contendo os três campos obrigatórios a seguir.

Parâmetros do Corpo (Body)
Parâmetro

Tipo

Descrição

Exemplo

solution

String

Nome da solução/produto que está solicitando o token.

"AiHelper"

clientId

String

Identificador único do cliente/empresa que usa a solução.

"123"

userId

String

Identificador único do usuário final que irá se conectar.

"Daniel"

Exemplo de Uso com curl
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "solution": "AiHelper",
        "clientId": "123",
        "userId": "Daniel"
      }' \
  https://token.aivoice.com.br

Resposta (Response)
Sucesso (200 OK)
Em caso de sucesso, a API retornará um objeto JSON com as informações necessárias para o cliente se conectar ao servidor LiveKit.

Campo

Descrição

token

O token de acesso JWT gerado.

room

O nome da sala gerado para a sessão.

identity

A identidade única do participante no contexto do LiveKit.

apiKey

A chave de API pública do servidor LiveKit.

Exemplo de Resposta:

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "AiHelper-123-Daniel",
  "identity": "AiHelper-123-Daniel",
  "apiKey": "APInroTUR7mKwUm"
}

Erros
400 Bad Request: A requisição não continha todos os campos obrigatórios.

500 Internal Server Error: Ocorreu um erro inesperado no servidor durante a geração do token.

3. Instalação e Manutenção (Para Backend/DevOps)
Esta seção descreve como instalar e gerenciar o serviço em uma nova VPS.

Pré-requisitos
Acesso root ou sudo na VPS.

Git instalado.

Python 3.8 ou superior.

Passos de Instalação
Clonar o Repositório

git clone git@github.com:seu-usuario/seu-repositorio.git
cd seu-repositorio

Criar Ambiente Virtual

python3 -m venv .venv
source .venv/bin/activate

Instalar Dependências

pip install -r requirements.txt

Criar Arquivo de Variáveis de Ambiente (.env)
Crie um arquivo chamado .env na raiz do projeto. Este arquivo NUNCA deve ser versionado.

cat <<'EOT' > .env
LIVEKIT_API_KEY="SUA_API_KEY_AQUI"
LIVEKIT_API_SECRET="SEU_SECRET_AQUI"
LIVEKIT_WS_URL="wss://live.aivoice.com.br"
EOT

Configuração como Serviço (Systemd)
Para garantir que a aplicação rode em segundo plano e inicie com o sistema, crie o seguinte arquivo de serviço.

Caminho: /etc/systemd/system/token-service.service

[Unit]
Description=Token Service FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/caminho/para/seu-repositorio
ExecStart=/caminho/para/seu-repositorio/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 3700
Restart=always

[Install]
WantedBy=multi-user.target

Comandos de Gerenciamento
Após criar o arquivo de serviço, use os seguintes comandos:

Habilitar o serviço para iniciar no boot:

sudo systemctl enable token-service

Iniciar o serviço:

sudo systemctl start token-service

Verificar o status:

sudo systemctl status token-service

Reiniciar o serviço (após alterações):

sudo systemctl restart token-service

Verificar logs em tempo real:

journalctl -u token-service -f

4. Segurança
CORS (Cross-Origin Resource Sharing)
A API está configurada para aceitar requisições apenas de subdomínios HTTPS de aivoice.com.br (ex: https://helper.aivoice.com.br). Isso é controlado pela expressão regular ^https:\/\/.*\.aivoice\.com\.br$ no middleware CORS, protegendo o serviço contra consumo por domínios não autorizados.

Variáveis de Ambiente
Todas as informações sensíveis, como as chaves de API do LiveKit, são gerenciadas através do arquivo .env. Este arquivo está listado no .gitignore e nunca deve ser enviado para o repositório Git.
