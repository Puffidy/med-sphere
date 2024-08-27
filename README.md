# MedSphere
Sistem koji olakšava praćenje pacijenta. U ovom programu biti ce moguće upisati pacijenta, prebaciti pacijenta i otpustiti.

## Funkcije

### CRUD
- `POST /patients`: Kreira novog pacijenta. Informacije o pacijentu su unutar request-body-ja u JSON formatu.
- `GET /patients`: Dohvaća sve pacijente.
- `GET /patients/:id`: Dohvaća jednog pacijenta na osnovu `id` parametra u ruti.
- `PUT /patients/:id`: Ažuriraj pacijenta na osnovu `id` parametra u ruti. Nove informacije o pacijentu su unutar request-body-ja u JSON formatu.
- `DELETE /patients/:id`: Izbriši pacijenta na osnovu `id` parametra u ruti.

### Dodatne funkcije
- `POST /patients/lowest-free`: Kreira novog pacijenta u prvom najnižem broju sobe. Informacije o pacijentu su unutar request-body-ja u JSON formatu.
- `POST /patients/:id/decursus`: Kreira novi decursus za pacijenta čiji je `id` u ruti. Informacije o decursus su unutar request-body-ja u JSON formatu.
- `GET /patients/without-decursus`: Dohvaća sve pacijente bez obavljenog dnevnog decursusa.
- `GET /patients/:id/decursus`: Dohvaća decursus-e za jednog pacijenta na osnovu `id` parametra u ruti.
- `PUT /patients/:id/release`: Otpušta pacijenta postavljanjem `released_at` atribut-a.
- `PUT /patients/:id/move/:new_room`: Prebaci pacijenta u novu sobu. Potrebni parametri su: pacijentov `id` i novi broj sobe.

## Instalacija
### Skidanje koda s GitHub-a 
```
git clone git@github.com:Puffidy/medi-sphere.git
cd medi-sphere
```
### Docker tutorial
```
docker-compose up 
```
Poslije toga otvorite localhost:3000 u vašem browser-u ili importirajte `postman_collection.json` u vašoj [postman aplikaciji](https://www.postman.com/) da bi testirali API-Call-ove


