#coding: utf-8

from pox.core import core
import pox.openflow.libopenflow_01 as of 
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
import pox.lib.packet as pkt

log = core.getLogger()

def _handle_PacketIn(event):

  packet = event.parsed
  msg = of.ofp_flow_mod()
  ##Mensagens de debug de classes do Python
  #print type(event)
  print packet.next.srcip
  print 
  
  if event.dpid == 1:
      print 'OK'
      if packet.next.dstip <"10.10.1.0":   
   
        log.info('match')
        msg.idle_timeout = 10                #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
        msg.match.dl_type=0x800              #dl_type do IPv4
    	msg.match.nw_dstip="10.10.1.0/24"      
    	msg.actions.append(of.ofp_action_output(port =of.OFPP_NORMAL))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
    	_reenvio(event)                      #Método p/tratamento dos primeiros paotes (evitar perda)
   
  #INSERIR AÇÃO DE ENVIAR PACOTES "PERDIDOS" (NÃO PERDER PRIMEIROS PACOTES DE CONFIGURAÇÃO)

    	#event.connection.send(msg) #Envia o novo fluxo p/ o switch que solicitou
      elif packet.next.dstip is (IPAddr("10.10.2.0"),24):
    	log.info('match 2')
    	msg.idle_timeout = 10
    	msg.match.dl_type=0x800
    	msg.match.nw_dst="10.10.2.0/24"
    	msg.actions.append(of.ofp_action_output(port=4))
    	_reenvio(event)
    
      elif packet.next.dstip is (IPAddr("10.10.3.0"),24):
       	log.info('match 2')
       	msg.idle_timeout = 10
       	msg.match.dl_type=0x800
       	msg.match.nw_dst="10.10.3.0/24"
       	msg.actions.append(of.ofp_action_output(port=5))             
       	_reenvio(event)
    	
    	
    	

def _reenvio(event):
    msg2 = of.ofp_packet_out()
    msg2.data = event.ofp
    msg2.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) #provisório
    event.connection.send(msg2)
    event.connection.send(msg)
    
def launch (reactive = True):  #Modo reativo ativado
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn) #Adiciona "escutador de evento" e associa o tratamento com '_handlePacketIn'
    log.info('CONTROLADOR INICIADO')
