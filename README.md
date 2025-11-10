## Discente - Andrei Boulhosa de Sant'Anna

# Atividade Individual 01 (AV3) - Sistemas Distribuídos

Este projeto implementa um ambiente distribuído composto por múltiplas instâncias de serviço (três containers backend) que são balanceadas por um proxy reverso Nginx.

O objetivo principal é entender e demonstrar na prática como o balanceamento de carga contribui para o **desempenho** (distribuição de requisições), **disponibilidade** (tolerância a falhas) e **escalabilidade** do sistema.

## 🏛️ Arquitetura do Ambiente

O ambiente é orquestrado utilizando Docker Compose e consiste nos seguintes serviços:

  * **`proxy` (Nginx):** Atua como o **Proxy Reverso** e **Balanceador de Carga**. Ele é o único ponto de entrada para o cliente (escutando na porta `80`) e distribui as requisições recebidas para os serviços backend.
  * **`web1` (FastAPI):** Instância 1 do serviço backend, executando em um container Docker.
  * **`web2` (FastAPI):** Instância 2 do serviço backend, executando em um container Docker.
  * **`web3` (FastAPI):** Instância 3 do serviço backend, executando em um container Docker.

Cada serviço backend possui um único endpoint (`/`) que retorna um JSON com informações sobre o servidor que atendeu a requisição, o timestamp, a latência simulada e o IP do cliente.

## Tecnologias Utilizadas

  * **Docker e Docker Compose:** Para criar, gerenciar e orquestrar os contêineres de aplicação.
  * **Nginx:** Utilizado como proxy reverso e balanceador de carga.
  * **FastAPI (Python):** Framework web usado para criar os serviços backend.

Para executar este projeto, você precisará de:

  * Docker
  * Docker Compose (geralmente incluído no Docker Desktop)
  * `curl` ou um navegador web (para testes manuais)
  * `ab` (Apache Benchmark) para testes de carga (Ex: `sudo apt install apache2-utils`)
  * `jq` (para filtrar a saída JSON da inspeção de rede - opcional, mas recomendado): `sudo apt install jq`

## Como Executar

1.  Clone este repositório para sua máquina local.

2.  Abra um terminal na pasta raiz do projeto.

3.  Execute o seguinte comando para construir as imagens e iniciar todos os contêineres:

    ```bash
    docker compose up --build -d
    ```

4.  Uma vez que os contêineres estejam em execução, você pode acessar o serviço através do proxy em:
    `http://localhost`

##  Como Verificar os IPs dos Contêineres (Opcional)

Para fins de depuração, pode ser útil ver os IPs internos que o Docker atribuiu a cada contêiner.

1.  Primeiro, descubra o nome da rede criada pelo Docker Compose:

    ```bash
    docker network ls
    # O nome será algo como "nome-da-pasta-do-projeto_default"
    # Ex: entrega_1_default
    ```

2.  Use o comando `docker network inspect` e filtre a saída com `jq` para mostrar apenas o nome e o IP de cada serviço:

    ```bash
    # Substitua 'entrega_1_default' pelo nome da sua rede
    docker network inspect entrega_1_default | jq '.[0].Containers | .[] | {name: .Name, ip: .IPv4Address}'
    ```

3.  O resultado será parecido com este, mostrando os IPs da rede interna:

    ```json
    {
      "name": "entrega_1-web1-1",
      "ip": "172.18.0.4/16"
    }
    {
      "name": "entrega_1-web2-1",
      "ip": "172.18.0.2/16"
    }
    {
      "name": "entrega_1-web3-1",
      "ip": "172.18.0.3/16"
    }
    {
      "name": "entrega_1-proxy-1",
      "ip": "172.18.0.5/16"
    }
    ```

## Análise dos Experimentos

Os testes a seguir foram realizados para analisar o comportamento dos diferentes algoritmos de balanceamento e a resiliência do sistema.

**Para alterar o algoritmo de balanceamento:**

1.  Pare o ambiente: `docker compose down`
2.  Edite o arquivo `proxy/nginx.conf`.
3.  Na seção `upstream backend_servers`, comente ou descomente a diretiva desejada (`least_conn;` ou `ip_hash;`).
4.  Reinicie o ambiente: `docker compose up --build -d`

-----

### Experimento 1: Round Robin (Padrão)

  * **Configuração:** Nenhuma diretiva de algoritmo foi especificada no bloco `upstream`, utilizando o padrão Round Robin do Nginx.

  * **Teste:** Múltiplas requisições foram enviadas ao `http://localhost` (atualizando o navegador) e um teste de carga foi executado com `ab -n 1000 -c 50 http://localhost/`.

  * **Coleta de Dados (Logs):** Os logs do Nginx foram coletados com `docker compose logs proxy`.

  ![Logs_Round_Robin](https://github.com/user-attachments/assets/6b04a406-473b-4e5b-931c-17154a06238b)

  

* **Análise:**
1000 requisições 

![Round_Robin_1000_requisições](https://github.com/user-attachments/assets/881b0ffd-6ede-4b72-95ba-8259e9eb7d8c)

10000 requisições

![Round_Robin_10000_requisições](https://github.com/user-attachments/assets/affb945a-8974-435d-8efe-2189df3c966e)

100000 requisições

![Round_Robin_100000_requisições](https://github.com/user-attachments/assets/d04763bd-2ef0-445c-9095-795a6ef27e9f)

Conforme observado nos logs e nos testes de navegador, o algoritmo Round Robin distribuiu as requisições de forma sequencial e equitativa entre os três servidores (web1, web2, web3, web1...). A distribuição de carga foi uniforme, com cada servidor recebendo aproximadamente 333 das 1000 requisições, 3333 das 10000 requisições e 33333 das 100000 requisições dos testes de carga ab.

-----

### Experimento 2: Least Connections

  * **Configuração:** A diretiva `least_conn;` foi descomentada no `nginx.conf`.

  * **Teste:** Teste de carga com `ab -n 1000 -c 50 http://localhost/`.
  * **Coleta de Dados (Logs):**
  
![Logs_Leans_conn](https://github.com/user-attachments/assets/5a0e8491-3ef6-4964-bd74-ab48207b2fbb)

  * **Análise:**

1000 requisições 

![learn_connection_1000_requisições](https://github.com/user-attachments/assets/f5590662-d0f0-4f06-8c70-c3adb0e4d629)


10000 requisições


![learn_connection_10000_requisições](https://github.com/user-attachments/assets/91cef213-44fd-48e3-9583-60ee54a86cb3)

100000 requisições

![learn_connection_100000_requisições](https://github.com/user-attachments/assets/332cba2a-7543-4f14-a018-690eb3c1f230)

    O algoritmo `least_conn` envia novas requisições para o servidor com o menor número de conexões ativas no momento. Como nossos endpoints têm uma latência simulada muito curta e uniforme, o comportamento foi muito similar ao Round Robin. Em um cenário real com requisições de duração variável, este algoritmo seria mais eficiente, prevenindo que um servidor fique sobrecarregado enquanto outros estão ociosos.*

-----

### Experimento 3: IP Hash

  * **Configuração:** A diretiva `ip_hash;` foi descomentada no `nginx.conf`.

  * **Teste:** Múltiplas requisições enviadas *a partir do mesmo navegador* e `curl` (mesmo IP de cliente).

  * **Coleta de Dados (Logs):**

    ![Logd_IP_Hash](https://github.com/user-attachments/assets/07bf2cd2-88e0-47f9-b7fd-27cf3f06a0dd)

  * **Análise:**
1000 requisições 

![IP_Hash_1000_requisições](https://github.com/user-attachments/assets/b9b8ff76-f34f-4054-875c-620975291da1)

10000 requisições

![IP_Hash_10000_requisições](https://github.com/user-attachments/assets/ec848bc9-e520-4317-adad-b20114998ef7)

100000 requisições

![IP_Hash_100000_requisições](https://github.com/user-attachments/assets/c0c52ff1-fbca-4a6a-b7c9-95142c5dc188)


  Este algoritmo direciona o cliente sempre ao mesmo servidor com base no hash do seu IP. Como esperado, todas as requisições do meu navegador e `curl` foram consistentemente roteadas para o mesmo servidor (`web1` no meu teste). Isso demonstra como o `ip_hash` é usado para manter a afinidade de sessão (session stickiness), o que é vital para aplicações que armazenam estado (como um carrinho de compras).*

-----

### Experimento 4: Teste de Tolerância a Falhas

  * **Configuração:** Ambiente executando com o balanceamento Round Robin.

  * **Teste:** Simulação da indisponibilidade de um dos serviços backend.

    1.  O ambiente estava operando normalmente, distribuindo entre web1, web2 e web3.
    2.  O serviço `web2` foi parado manualmente: `docker compose stop web2`
    3.  Novas requisições foram enviadas para `http://localhost`.

  * **Coleta de Dados (Logs):**

  * Log

![logs_teste_sem_web2](https://github.com/user-attachments/assets/4c2ba221-0031-431b-9afc-3b81e647db2d)

    

  * **Análise:**

    * Imediatamente após parar o container `web2`, o Nginx detectou que o servidor não estava respondendo e automaticamente o removeu do pool de balanceamento. O serviço em `http://localhost` continuou funcionando perfeitamente, sem qualquer erro para o cliente. Os logs confirmam que o tráfego passou a ser distribuído apenas entre os servidores saudáveis (`web1` e `web3`). Isso demonstra a capacidade do proxy reverso de garantir alta disponibilidade.*

## 🎬 Vídeo de Demonstração

[COLE O LINK PÚBLICO PARA O SEU VÍDEO DE 2 MINUTOS AQUI]

