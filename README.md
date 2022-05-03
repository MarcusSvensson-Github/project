Webbshop
Inledning
En annonssida där användare kan lägga upp produkter de vill sälja likt blocket och facebook market. En säljare ska kunna lägg upp sina produkter på hemsidan. En köpare ska kunna söka efter produkter och om en matchande produkt ska köparen kunna klicka in på sidan för produkten. På denna sida finns information om säljaren som email, telefonnummer. Endast säljare som vill lägga upp en annons behöver ett konto.

Databas som innehåller annonser och användare, relationen är att en användare äger en eller flera annonser. En server som sköter kommunikationen mellan databasen och klienten samt bearbetar information.

Databasen kommer att skapas i MySQL.

Servern kommer kodas i python (django eller flask) och kommunicera med databasen med hjälp av pymySQL modulen. Kommunikation med gränssnittet kommer att göras med python modulen http.server som använder protokollet HTTP och ramverket AJAX. 
Gränssnittet kommer bestå av HTML sidor med CSS och javascript.
Vid besök av webben möts personen av en indexsida över annonser. Personen kan välja att söka produkter för att dynamisk filtrera innehållet eller trycka på en befintlig annons. Trycker personen på en befintlig annons kommer den till en ny sida där information om användaren som äger annonsen finns. Personen kan även gå tillbaka till indexsidan. En person kan även logga eller skapa ett konto. Som inloggad ser användaren sina annonser och kan skapa nya.



