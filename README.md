# TrabRedesMininet


1- COMO USAR O PROGRAMA?


2- TOPOLOGIA
  Antes de tudo e necessario definir a topologia da rede ,ou seja, como os hosts e switchs estao posicionados e interligados dentro da rede. Essas definicoes encontram-se na class MyTopo.
  Montamos uma topologia simples com o objetivo de simular dois laboratorios do DINF, onde as maquinas de cada laboratorio estao ligados a um switch, um switch por laboratorio, e por fim esses switchs ligados ao switch principal q interliga os labs. Segue ilustracao da topologia:

                                    switch-1
                                      /\
                                     /  \
                                    /    \
                            switch-2      switch-3
                          /   /   /        \   \   \    
                       h-1  h-2  h-3     h-4   h-5  h-6

        h = host
        / ou \ = link

  A topologia em arvore e simples mas que possibilita os testes desejados , provocando-os na rede e indentificando-os. O numero de hosts por laboratorio esta predefinida em 3 mas pode ser alterada atraves da variavel "numHost_per_Switch".

3- TESTES
  3.1- Teste de congestionamento
    Antes de identificar o problema na rede e necessario provoca-lo, feito atraves da funcao createCongest() que cria um fluxo de dados entre servidor -> cliente, no nosso caso o servidor = host-2 e cliente = host-1,
    congestionando o link switch-2 -> h-1
    Para identificacao do problema, e enviado pacotes de teste de algum host para todos os outros com a comando "ping". Analisando os resultados do comando e possivel ver a latencia dos pacotes, onde essa e muito maior quando envia-se para host-1 diferente do envio para outros hosts, um resumo da saida de "ping":

    De host-3 para host-1 / latencia = 1000ms
    De host-3 para host-2 / latencia = 70ms
    De host-3 para host-3 / latencia = 0ms
    De host-3 para host-4 / latencia = 130ms
    De host-3 para host-5 / latencia = 140ms
    De host-3 para host-6 / latencia = 120ms

    E visivel a demora do pacote chegar em host-1. Para o pacote chegar em host-2 que tem caminho equivalente a h-1 demora 70ms e para chegar nos hosts h-4,h-5,h-6 demora mais, pois esses estao em outro laboratorio
