# TrabRedesMininet

Autores:


1- COMO USAR O PROGRAMA?

  Execute o arquivo python com o comando, em modo kernel:
    sudo python Topology.py [-c ou -f ou -b ou -h]

  Escolha entre quais testes quer realizar:
    -c , para causar um congestionamento na rede e realizar os devidos testes para identificacao do problema
    -f , para causar um erro de encaminhamento e realizar os devidos testes para identificacao do problema
    -b , para testes de avaliacao na largura de banda
    -h , impressao da ajuda no terminal

2- TOPOLOGIA
  Antes de tudo e necessario definir a topologia da rede ,ou seja, como os hosts e switchs estao posicionados e interligados dentro da rede. Essas definicoes encontram-se na class MyTopo.
  Montamos uma topologia simples com o objetivo de simular dois laboratorios do DINF, onde as maquinas de cada laboratorio estao ligados a um switch, um switch por laboratorio, e por fim esses switchs ligados ao switch principal q interliga os labs. Segue ilustracao da topologia:

                                    switch-1
                                      /\
                                     /  \
                                    /    \
                            switch-2      switch-3
                          /   /   /        \   \   \
                       h-1  h-2  h-3      h-4   h-5  h-6

        h = host
        / ou \ = link

  A topologia em arvore e simples mas que possibilita os testes desejados , provocando-os na rede e indentificando-os. O numero de hosts por laboratorio esta predefinida em 3 mas pode ser alterada atraves da variavel "numHost_per_Switch".

3- TESTES
  3.1- Erro de Encaminhamento
    Antes de identificar o problema na rede e necessario provoca-lo, entao e criado um host chamado host_brokens, e um link danificado entre ele e o switch-1, simulamos esse transtorno aumentando a perda no link (loss = 20).Para identificacao do problema, e enviado pacotes de teste de algum host (hostTest) para todos os outros com a comando "ping", atraves do metodo ping_oneHost_to_allHosts(). Com a analise dos resultados vemos que a perda de pacotes entre o hostTeste e o host com link "corrompido" e maior que outras comunicacoes, um exemplo dos resultados abaixo:

      De hostTest para host-1 / loss = 0% packet loss
      De hostTest para host-2 / loss = 2% packet loss
      De hostTest para host-3 / loss = 0% packet loss
      De hostTest para host-4 / loss = 25% packet loss
      De hostTest para host-5 / loss = 0% packet loss
      De hostTest para host-6 / loss = 12% packet loss
      De hostTest para host_broken / loss = 62% packet loss

    Logo, podemos verificar que existe perda de pacotes entre hostTest -> host_broken, pela alta de loss e identificamos que o link de host_broken ao switch, pois a perda so ocorre sobre o host_broken.
    Caso outros envios estivessem com perdas tambem, descobririamos que o link "danificado" seria o link em comum entre os hosts que nao receberam mensagens , por exemplo, tomando hostTest = host-5 e tendo os seguintes resultados dos testes:

      De host-5 para host-1 / loss = 60% packet loss
      De host-5 para host-2 / loss = 59% packet loss
      De host-5 para host-3 / loss = 70% packet loss
      De host-5 para host-4 / loss = 8% packet loss
      De host-5 para host-5 / loss = 0% packet loss
      De host-5 para host-6 / loss = 12% packet loss

    Sabendo que os hosts (h1,h2,h3) compartilham o mesmo link entre switch-1 e switch-2, descobreriamos que este link seria o "corrompido", pois e o link em comum entre os hosts no caminho dos pacotes de teste enviados por h-5.


  3.2- Teste de congestionamento
    Como visto e preciso provocar o problema, feito atraves da funcao createCongest() que cria um fluxo de dados entre servidor -> cliente, no nosso caso o servidor = host-2 e cliente = host-1,
    congestionando o link switch-2 -> h-1
    Para identificacao do problema, e enviado pacotes de teste de algum host para todos os outros com a comando "ping". Analisando os resultados do comando e possivel ver a latencia dos pacotes, onde essa e muito maior quando envia-se para host-1 diferente do envio para outros hosts, um resumo da saida de "ping":

      De host-3 para host-1 / latencia = 1000ms
      De host-3 para host-2 / latencia = 70ms
      De host-3 para host-3 / latencia = 0ms
      De host-3 para host-4 / latencia = 130ms
      De host-3 para host-5 / latencia = 140ms
      De host-3 para host-6 / latencia = 120ms

    E visivel a demora do pacote chegar em host-1. Para o pacote chegar em host-2 que tem caminho equivalente a h-1 demora 70ms e para chegar nos hosts h-4,h-5,h-6 demora mais, pois esses estao em outro laboratorio

  3.3 - Teste de largura de banda
