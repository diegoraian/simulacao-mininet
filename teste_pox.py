#coding: utf-8

from pox.core import core
import pox.openflow.libopenflow_01 as of 
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
import pox.lib.packet as pkt

log = core.getLogger()

def _handle_PacketIn(event):

 
  msg = of.ofp_flow_mod()
  packet = event.parsed
  log.info('pacote recebido com type: %d',packet.type)
  msg_old = of.ofp_packet_out()
  msg_old.data = event.ofp
  msg_old.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

  
  if packet.type==2048:   
    #if event.port == 1:
    log.info('match')
    msg.match.dl_type=0x800
    msg.match.nw_src="10.0.0.0/24"       #AJUSTAR IP
    msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      
   # elif event.port == 2:
     # log.info('match 2')
     # msg.match.dl_type=0x800
     # msg.match.nw_src="10.0.0.2"       #AJUSTAR IP
     # msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))

  elif packet.type==2054:
    log.info('match 2')
    msg.match.dl_type=0x806
    msg.match.nw_src="10.0.0.0/24"       #AJUSTAR I
    msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
    
  # elif event.port == 2:
  #  log.info('match 2')   # msg.match.dl_type=0x806
  # msg.match.nw_src="10.0.0.2"       #AJUSTAR IP
  # msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))

  
  #INSERIR AÇÃO DE ENVIAR PACOTES "PERDIDOS" (NÃO PERDER PRIMEIROS PACOTES DE CONFIGURAÇÃO)

  event.connection.send(msg) #ENVIA O FLUXO PARA O SWITCH
  
  

def launch (reactive = True):
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info('CONTROLADOR INICIADO')
