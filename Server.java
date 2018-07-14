import java.net.BindException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Date;

public class Server {
	private static final Integer PORTA = 6001;

	public static void main(String[] args) {

		DatagramSocket serverSocketUDP = null;
		System.out.println("Sincronizador funcionando");
		while (true) {
			try {
				serverSocketUDP =  new DatagramSocket(PORTA);
				Thread.currentThread().sleep(1000);
				byte[] bufferConsulta = new byte[12];
				DatagramPacket pacote = new DatagramPacket(bufferConsulta, 12);
				serverSocketUDP.receive(pacote);
				String ipServidor = new String(pacote.getData(),StandardCharsets.UTF_8);
				System.out.println("Pacote recebido " + ipServidor);
				if(ipServidor != null && !ipServidor.isEmpty()) {
					
					Date date = new Date();
					date.getTime();
					InetAddress ip = InetAddress.getByName(ipServidor);
					String mensagem = date.toString();
					byte[] buffer = mensagem.getBytes(StandardCharsets.UTF_8);
					System.out.println(buffer.length);
					DatagramPacket pacoteEnvio = new DatagramPacket(buffer, buffer.length, ip, PORTA);
					serverSocketUDP.send(pacoteEnvio);
					System.out.println("Pacote enviado " + mensagem);
					serverSocketUDP.close();
				}
				serverSocketUDP.close();
			} catch(BindException be) {
				System.out.println(be.getMessage());
			}catch (Exception e) {
				if (serverSocketUDP != null) {
					serverSocketUDP.close();
				}
				e.printStackTrace();
			}

		}
	}
	
}