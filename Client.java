
import java.io.IOException;
import java.net.BindException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Client {
	private static final Integer PORTA = 6001;

	public static void atualizarHorario(Date data) throws IOException {
		SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/YYYY hh:mm");
		String dataString = dateFormat.format(data);
		String dia =dataString.substring(0, 2);
		String mes = dataString.substring(4,6);
		String ano = dataString.substring(8,10);
		String hora = dataString.substring(12,14);
		String minuto = dataString.substring(12,14);
		//Atualiza o tempo no linuxformado 'dd/MM/YYYY hh:mm';
		Runtime.getRuntime().exec("date -s "+dia+"/"+mes+"/"+ano+" "+hora+":"+minuto);
	}
	
	public static void main(String[] args) throws Exception {
		
		if(args.length > 0 &&  args[0] != null) {
		  System.out.println("Cliente está funcionando");
		  IP_SERVIDOR = args[0];
		  System.out.println("IP DO SERVIDOR:");
		  System.out.println(IP_SERVIDOR);
		}else{
			throw new Exception("Não foi inserido o endereço do servidor NTP_FAKE ");
		};
		DatagramSocket serverSocketUDP = null;
		while (true) {
			try {
					Thread.currentThread().sleep(2000);
					serverSocketUDP = new DatagramSocket(PORTA);
					Date date = new Date();
					date.getTime();
					byte[] buffer = new byte[28];
					DatagramPacket pacote = new DatagramPacket(buffer, 28);
					serverSocketUDP.receive(pacote);
					
					String mensagem = new String(pacote.getData(),StandardCharsets.UTF_8);
					System.out.println("Pacote recebido " + mensagem);
					serverSocketUDP.close();
					Date dataRecebida= new Date(new Date().parse(mensagem));					
					atualizarHorario(dataRecebida);
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