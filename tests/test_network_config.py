# Importerar pytest, som används för att skapa och köra tester
import pytest
# Importerar NetworkConfigManager-klassen som ska testas
from network_config_manager import NetworkConfigManager
 
# Skapar en pytest fixture som hanterar setup och teardown för NetworkConfigManager
# Denna fixture körs före varje test för att skapa och återställa manager-objektet
@pytest.fixture
def manager():
    # Skapar en nytt obeject av NetworkConfigManager
    manager = NetworkConfigManager()
    # Ansluter till manager
    manager.connect()
 
    # Återställer konfigurationerna till deras standardvärden efter att testet är klart
    manager.update_hostname("1")  
    manager.update_interface_state("down")  
    manager.update_response_prefix("Standard Response")
 
    # Yield gör att pytest kan använda manager-objektet i testen
    yield manager
 
    # Efter att testet har kört och yield har använts, disconnectas manager-objektet
    manager.disconnect()
 
# Testklass som innehåller alla tester för NetworkConfigManager
class TestNetworkConfigManager:
    # Testmetod som verifierar att standardvärdet för hostname är korrekt.
    def test_show_hostname_default(self, manager):
        # Verifierar att hostname är "1" som är standardvärdet
        assert manager.show_hostname() == "hostname: 1"
 
    # Testmetod som verifierar att standardvärdet för interface state är korrekt
    def test_show_interface_state_default(self, manager):
        # Verifierar att interface state är "down" som är standardvärdet
        assert manager.show_interface_state() == "interface_state: down"
 
    # Testmetod som verifierar att standardvärdet för response prefix är korrekt
    def test_show_response_prefix_default(self, manager):
        # Verifierar att response prefix är "Standard Response" som är standardvärdet
        assert manager.show_response_prefix() == "response_prefix: Standard Response"
 
    # Testmetod som testar uppdatering av hostname
    def test_update_hostname(self, manager):
        # Uppdaterar hostname till "RouterX"
        manager.update_hostname("RouterX")
        # Verifierar att hostname nu är "RouterX"
        assert manager.show_hostname() == "hostname: RouterX"
 
    # Testmetod som testar uppdatering av interface state
    def test_update_interface_state(self, manager):
        # Uppdaterar interface state till "up"
        manager.update_interface_state("up")
        # Verifierar att interface state nu är "up"
        assert manager.show_interface_state() == "interface_state: up"
 
    # Testmetod som testar uppdatering av response prefix
    def test_update_response_prefix(self, manager):
        # Uppdaterar response prefix till "CustomPrefix:"
        manager.update_response_prefix("CustomPrefix:")
        # Verifierar att response prefix nu är "CustomPrefix:"
        assert manager.show_response_prefix() == "response_prefix: CustomPrefix:"
 
    # Testmetod som testar uppdatering och verifiering av hostname
    def test_update_and_verify_hostname(self, manager):
        new_hostname = "NewRouter"
        # Uppdaterar hostname till "NewRouter"
        manager.update_hostname(new_hostname)
        # Verifierar att hostname nu är "NewRouter"
        assert manager.show_hostname() == f"hostname: {new_hostname}"
 
    # Testmetod som testar uppdatering och verifiering av interface state
    def test_update_and_verify_interface_state(self, manager):
        new_state = "up"
        # Uppdaterar interface state till "up"
        manager.update_interface_state(new_state)
        # Verifierar att interface state nu är "up"
        assert manager.show_interface_state() == f"interface_state: {new_state}"
 
    # Testmetod som testar uppdatering och verifiering av response prefix
    def test_update_and_verify_response_prefix(self, manager):
        new_prefix = "NewResponsePrefix:"
        # Uppdaterar response prefix till "NewResponsePrefix:"
        manager.update_response_prefix(new_prefix)
        # Verifierar att response prefix nu är "NewResponsePrefix:"
        assert manager.show_response_prefix() == f"response_prefix: {new_prefix}"
 
    # Testmetod som testar att ett fel kastas vid ogiltig interface state
    def test_update_and_verify_interface_state_exception(self, manager):
        new_state = "left"  # Ett ogiltigt värde för interface state
        # Förväntar sig ett ValueError undantag när man försöker sätta ett ogiltigt värde
        with pytest.raises(ValueError):
            manager.update_interface_state(new_state)