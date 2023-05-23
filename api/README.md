# Reverse Engineering Spotify for Artists Private API

## Autenticación

Para acceder a Spotify for Artists es necesaria una cuenta de usuario de Spotify. Una vez iniciada sesión, se comprueba el listado de artistas a los que el usuario tiene acceso y el nivel de acceso que éste tiene.

### Flujo de autenticación

Al igual que con la API de Spotify, para poder realizar peticiones a la API Privada de Spotify for Artists es necesario obtener un _token_ de acceso válido. Para poder obtener dicho token se sigue el siguiente flujo:

1. Acceder a la URL de autenticación de Spotify: https://accounts.spotify.com.
2. Ingresar usuario y contraseña que permiten obtener un código de autenticación.
3. Utilizar el código de autententicación para obtener un token de acceso y un token de actualización.
4. Utilizar el token de actualización cuando el token de acceso caduque para obtener uno nuevo.

## Spotify for Artists Private API

El endpoint de la API privada de Spotify for Artists es: 


# Reverse Engineering Amazon for Artists Private API

## Autenticación

### Flujo de autenticación

Una vez autenticado, se proporciona una cookie de sesión que es necesaria para acceder a la información. Además hay que indicar un token "x-csrf-token"

## Amazon for Artists Private API

### Endpoints

POST https://user.artists.amazon.com/V1/web/usermanagement/register
POST https://team.artists.amazon.com/V1/web/teammanagement/teams/get
POST https://invite.artists.amazon.com/V1/web/invitemanagement/B00F6N65G4/invite/list

### Ejemplos

POST `https://user.artists.amazon.com/V1/web/usermanagement/register`
- Cabeceras: cookie, x-csrf-token
- Respuesta:
```
{
    "oAuthClientIds": {
        "TUNECORE": "74I5MT8KWslomqzneg7w",
        "DISTROKID": "4433DEFB-0228-4249-A976AE67EBC230B2",
        "INSTAGRAM": "480975089492568",
        "TWITCH": "ova6o1oygt8pjkqmyibv4a5a4byxd6",
        "FACEBOOK": "480975089492568",
        "TWITTER": "cGCCGFu9PAbFqWxzrcFLk7dEj",
        "CDBABY": "910876ba-7347-47bc-9de0-4907c18fe48f"
    },
    "teamInfos": [
        {
            "artistAsins": [
                "B00F6N65G4"
            ],
            "createdDate": "2020-03-28T23:40:41.655Z",
            "description": "Mpv",
            "members": [
                {
                    "company": "MPV",
                    "jobTitle": "Artist",
                    "memberId": "1485b0bf-8458-48a0-bd5e-b61fb0ddc5e6",
                    "name": "Mariano Palomo Villafranca",
                    "permissions": [
                        "AddMember",
                        "PromoteToOwner",
                        "RemoveMember",
                        "SetPermissions",
                        "SetMemberInfo",
                        "ReadReports",
                        "SendInvite",
                        "CancelInvite",
                        "ListInvites",
                        "UploadImage",
                        "ManageBluePrints",
                        "ManageTwitch"
                    ],
                    "role": "Owner"
                }
            ],
            "teamId": "B00F6N65G4",
            "teamName": "Mpv",
            "teamType": "ARTIST",
            "updatedDate": "2020-03-28T23:40:41.655Z"
        },
        {
            "artistAsins": [
                "B01BUH5IJE"
            ],
            "createdDate": "2020-11-18T17:11:30.904Z",
            "description": "I'm currently managing Jomy Galan profiles as part of Naz4ri Music where he's a composer and artist. ",
            "members": [
                {
                    "company": "Jomy Galan",
                    "jobTitle": "Manager",
                    "memberId": "3cc9df30-94b8-4a34-8159-b46949c4d01e",
                    "name": "Mariano Palomo Villafranca",
                    "permissions": [
                        "AddMember",
                        "PromoteToOwner",
                        "RemoveMember",
                        "SetPermissions",
                        "SetMemberInfo",
                        "ReadReports",
                        "SendInvite",
                        "CancelInvite",
                        "ListInvites",
                        "UploadImage",
                        "ManageBluePrints",
                        "ManageTwitch"
                    ],
                    "role": "Owner"
                }
            ],
            "teamId": "B01BUH5IJE",
            "teamName": "Jomy Galan",
            "teamType": "ARTIST",
            "updatedDate": "2020-11-18T17:11:30.904Z"
        },
        {
            "artistAsins": [
                "B01HJRG7Q2"
            ],
            "createdDate": "2020-11-18T17:23:42.628Z",
            "description": "I'm currently managing 4BEATs profiles as part of Naz4ri Music where he's a producer and artist. ",
            "members": [
                {
                    "company": "4BEATs",
                    "jobTitle": "Manager",
                    "memberId": "100ceb74-98a4-400e-9387-0e8bcfcbf216",
                    "name": "Mariano Palomo Villafranca",
                    "permissions": [
                        "AddMember",
                        "PromoteToOwner",
                        "RemoveMember",
                        "SetPermissions",
                        "SetMemberInfo",
                        "ReadReports",
                        "SendInvite",
                        "CancelInvite",
                        "ListInvites",
                        "UploadImage",
                        "ManageBluePrints",
                        "ManageTwitch"
                    ],
                    "role": "Owner"
                }
            ],
            "teamId": "B01HJRG7Q2",
            "teamName": "4beats",
            "teamType": "ARTIST",
            "updatedDate": "2020-11-18T17:23:42.628Z"
        },
        {
            "artistAsins": [
                "B085BBTFNC"
            ],
            "createdDate": "2020-12-04T05:42:36.739Z",
            "description": "I'm currently managing Niko Rosé profiles as part of Naz4ri Music where he's a composer and artist. ",
            "members": [
                {
                    "company": "Niko Rosé",
                    "jobTitle": "Manager",
                    "memberId": "facd7f0a-e174-477c-9770-824de4435cc2",
                    "name": "Mariano Palomo Villafranca",
                    "permissions": [
                        "AddMember",
                        "PromoteToOwner",
                        "RemoveMember",
                        "SetPermissions",
                        "SetMemberInfo",
                        "ReadReports",
                        "SendInvite",
                        "CancelInvite",
                        "ListInvites",
                        "UploadImage",
                        "ManageBluePrints",
                        "ManageTwitch"
                    ],
                    "role": "Owner"
                }
            ],
            "teamId": "B085BBTFNC",
            "teamName": "Niko Rosé",
            "teamType": "ARTIST",
            "updatedDate": "2020-12-04T05:42:36.739Z"
        }
    ],
    "userSettings": {
        "acceptedTermsSetting": true,
        "betaEmailSetting": "OPT_OUT",
        "marketingEmailSetting": "OPT_OUT",
        "userLocaleSetting": "es_ES"
    }
}
```

POST https://team.artists.amazon.com/V1/web/teammanagement/teams/get
- Cabeceras: cookie, x-csrf-token
- Respuesta:
```

```

POST https://invite.artists.amazon.com/V1/web/invitemanagement/B00F6N65G4/invite/list
- Cabeceras: cookie, x-csrf-token
- Respuesta:
```

```
