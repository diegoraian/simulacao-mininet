#coding: utf-8

from pox.core import core
import pox.openflow.libopenflow_01 as of 
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
import pox.lib.packet as pkt
from pox.lib.util import dpid_to_str

log = core.getLogger()

def _handle_PacketIn(event):

  packet = event.parsed    # packet armazena o pacote do evento (event) de forma analisada
  msg = of.ofp_flow_mod()  #instacia um objeto do tipo ofp_flow_mod que servirá para inserir novos fluxos (regras) no switch
   
  
  print '***********************'
  ip_addr = packet.next.dstip.toStr() #Converte o IPv4 de destino em packet para string;
  

  print '******* EVENTO **********'
  print 'IP:'+ip_addr+'--subrede:'+str(getSubRede(ip_addr)) 
  print 'subnet: '+str(getSubRede(ip_addr)) 
  print 'porta: '+str(getPorta(ip_addr))  
  

  msg.idle_timeout=20    # Alteramos o  Tempo de Vida de um fluxo sem uso (tempo em segundos)
  msg.match.dl_type = 0x800   # Valor do IPv4 para match quando um pacote chegar ao switch. Esse valor de match será para todas as regras 
  
############################################################## CONFIG SUBREDE 10.10.1.0/24 
  if event.dpid == 1:
    print 'SWITCH 1 '
    if  getSubRede(ip_addr) == 1:   #Valores para a subrede 10.10.1.0/24
      print 'S1 puro'
      msg.match.nw_dst ="10.10.1."+str(getPorta(ip_addr))      
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                                   #Método p/tratamento dos primeiros pacotes (evitar perda)
       
    	
    elif getSubRede(ip_addr) == 2:
      print 'S1 para S2'  
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event, 4)
      
    
    elif getSubRede(ip_addr) == 3: 
      print 'S1 para S3'
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))             
      _reenvio(event,5)
     
      
# ############################################################## CONFIG SUBREDE 10.10.2.0/24 
  
  elif event.dpid == 2:
    print 'SWITCH 2 OK'
    if getSubRede(ip_addr) == 2: #Valores para a subrede 10.10.2.0/24
      print 'S2 puro'
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                      #Método p/tratamento dos primeiros paotes (evitar perda)
      
  
    elif getSubRede(ip_addr) == 1:
      print 'S2 para S1'
      msg.match.nw_dst= "10.10.1."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event,4)

    elif getSubRede(ip_addr) == 3:
      print 'S2 para S3'
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))					
      _reenvio(event,5)
	  
    
############################################################## CONFIG SUBREDE 10.10.3.0/24  
  
  elif event.dpid == 3:
    print 'SWITCH 3 OK'
    if getSubRede(ip_addr) == 3:      #Valores para subrede 10.10.3.0/24
      print 'S3 puro'
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                      #Método p/tratamento dos primeiros paotes (evitar perda)
      
				        
    elif getSubRede(ip_addr) == 1:
      print 'S3 para S1'
      msg.match.nw_dst= "10.10.1."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event,4)
      #event.connection.send(msg)

    elif getSubRede(ip_addr) == 2:
      print 'S3 para S2'
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))
      _reenvio(event,5)

    
  event.connection.send(msg) #Envia a regra pro switch    
      


  
def getPorta(ip_addr):              # Função que retorna o valor do ultimo octeto (porta de saida)
  return int(ip_addr.split('.')[3])  #pega a porta de determinado host-destino baseado no seu ip --> 10.10.1.2 = porta 2  
  
def getSubRede(ip_addr):           # Retorna a subrede que é informada no IP destino
  return int(ip_addr.split('.')[2])    	

def _reenvio(event, porta):       # MÉTODO PARA REENVIAR O 1o PACOTE (pacote gerador do evento),  PARA QUE NÃO HAJA PERDA
   msg2 = of.ofp_packet_out()  #cria uma instancia da classe ofp_packet_out (objeto de pacote de saída)
   msg2.data = event.ofp      # a estrutura de dados '.data' de msg2 receberá os valores do pacote que gerou o evento
   msg2.actions.append(of.ofp_action_output(port = porta)) # Ordena que quando esse tipo de mensagem chegar, o switch envie esse pacote para a porta indicada pelo parâmetro 'porta' (int)
   event.connection.send(msg2)  # Envia esta regra para o switch
    
    
def launch (reactive = True):  # Método que inicia o controlador / Modo reativo ativado
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn) #Adiciona "escutador de evento" e associa o tratamento com '_handlePacketIn'
    log.info('CONTROLADOR INICIADO - MODO REATIVO ATIVADO (IDLE TIMEOUT = 20s)')  # Texto exibido no log do controlador
