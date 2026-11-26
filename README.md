# Robo Vídeos Virais

Automação independente para selecionar vídeos de produtos recebidos de fontes autorizadas, validar links de afiliado e publicar até 10 vídeos por dia em uma Página do Facebook.

## Estado atual

- [x] Integração inicial com um publicador de Facebook já existente: **Graphpost**.
- [x] Adaptador próprio para chamar o Graphpost com vídeo local e legenda.
- [x] Execução segura por padrão: o adaptador faz **dry-run**; só publica com a opção explícita `--publish`.
- [x] Dependência fixada em um commit específico e validação automática no GitHub Actions.
- [x] Arquivos temporários, sessões e credenciais ignorados pelo Git.
- [ ] Entrada de vídeos do Telegram.
- [ ] Filtros de qualidade, deduplicação e seleção das 10 publicações diárias.
- [ ] Conversão de links para a conta de afiliado do proprietário.
- [ ] Fluxo completo de ponta a ponta e teste real autorizado na Página.

## Componente reaproveitado: Graphpost

O projeto usa [ghassenbrg/graphpost](https://github.com/ghassenbrg/graphpost), um publicador Python para Facebook Reels/vídeos via Meta Graph API.

- Licença do projeto original: MIT.
- Versão fixada: commit `157753f7d4dd4a90ebec6745b68e3b665586e61d`.
- Recurso aproveitado: envio de vídeo local para uma Página do Facebook e publicação como Reel.
- Requisito: Python 3.12+.
- O projeto original informa que seus testes simulam respostas da Meta; por isso, a integração ainda precisa ser validada com uma Página real.

O código original não foi copiado integralmente: o repositório instala a dependência licenciada e usa um adaptador pequeno para manter a integração isolada e atualizável.

## Como instalar localmente

```bash
python -m pip install -r requirements.txt
```

## Adaptador de publicação

O arquivo `publish_facebook.py` recebe um vídeo que já esteja disponível localmente.

Primeiro, configure as variáveis de ambiente:

- `FB_PAGE_ID`: ID da Página do Facebook.
- `GRAPHPOST_PAGE_TOKEN`: token de acesso da Página.

Nunca coloque tokens no código, em commits, prints ou mensagens. No GitHub, as credenciais deverão ser cadastradas em **Settings → Secrets and variables → Actions**.

### Simulação (padrão)

```bash
python publish_facebook.py --video caminho/do/video.mp4 --caption "Legenda e link de afiliado"
```

A simulação não publica nem envia o vídeo à Meta.

### Publicação real (somente após configurar e validar as permissões)

```bash
python publish_facebook.py --video caminho/do/video.mp4 --caption "Legenda e link de afiliado" --publish
```

A opção `--draft` envia o vídeo à Meta para criar um rascunho não publicado; portanto, também transfere o arquivo.

## Por que o coletor do Telegram ainda não foi incorporado

Os projetos avaliados para baixar histórico do Telegram usam uma sessão de conta via Telethon ou exigem um servidor persistente. Isso não se encaixa diretamente no GitHub Actions gratuito e pode exigir autenticação privada da conta. Um dos candidatos também não declara licença de reutilização. Não vamos copiar código sem licença clara nem armazenar uma sessão pessoal em um repositório.

Para receber novas mensagens automaticamente, a alternativa mais simples é um bot adicionado pelos administradores aos grupos/canais de origem, com as permissões corretas. Bots não conseguem ler o histórico anterior só porque receberam o link público do grupo. Para vídeos antigos, precisaremos de um arquivo/exportação autorizado ou outro acesso permitido.

## Próximos módulos

1. Coletor autorizado do Telegram (novas mensagens primeiro).
2. Fila temporária de vídeos e deduplicação por ID/hash.
3. Validação do produto e geração do link pela API oficial de afiliados Shopee.
4. Filtros e limite diário de 10 publicações.
5. Publicação Facebook, registro de resultados e limpeza do arquivo temporário.

## Custos e limites

Python, GitHub Actions, Telegram Bot API e Meta Graph API não exigem uma assinatura de software para começar, mas possuem limites, requisitos de conta, permissões e cotas. O uso do GitHub Actions depende da franquia disponível na conta. Não há chamadas pagas de IA neste estágio.

Vídeos só devem ser reutilizados quando houver autorização do titular dos direitos. Acesso público a um grupo não significa autorização automática para republicar o conteúdo.
