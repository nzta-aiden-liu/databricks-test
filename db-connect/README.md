1. In GitHub Codespace, forward a port like '8020', then copy the url, like `https://obscure-space-palm-tree-7v5xpprrg5492pgw4-8020.app.github.dev` (orginal_url), then url encode it as `https%3A%2F%2Fobscure-space-palm-tree-7v5xpprrg5492pgw4-8020.app.github.dev` (encoded_url).
2. In Databricks Account space, add orginal_url in `settings -> App connections`, then save the clientID.
3. Run [oauth_u2m_access_code_generator.py](./oauth_u2m_access_code_generator.py) and get `code_verifier` and `code_challenge`.
4. Assembly the first url:
```
https://<databricks_instance>/oidc/v1/authorize
?client_id=<clientID>
&redirect_uri=<encoded_url>
&response_type=code
&state=<identifier_string>
&code_challenge=<code_challenge_from_python_script>
&code_challenge_method=S256
&scope=all-apis+offline_access
```

5. Copy assembled url to browser, then provide user credentials to login, the browser will redirect back to a url, like:
```
https://<orginal_url>
?code=<returned_code_string>
&iss=https%3A%2F%2F<databricks_instance>%2Foidc
&state=<identifier_string>
```
Save the returned_code_string from the url.

6. Assembly the second url and paste and run in console
```
curl --request POST \
https://<databricks_instance>/oidc/v1/token \
--data "client_id=<clientID>" \
--data "grant_type=authorization_code" \
--data "scope=all-apis offline_access" \
--data "redirect_uri=<encoded_url>" \
--data "code_verifier=<code_verified_from_python_script>" \
--data "code=<returned_code_string>"
````

7. It should return:
```
{
    "access_token":"...",
    "refresh_token":"...",
    "scope":"all-apis offline_access",
    "token_type":"Bearer",
    "expires_in":3600
}
```
With ~/.databrickscfg file like:
```
[dev]
host=https://<databricks_instance>
token=<token>
```
Copy the `access_token` and paste in ~/.databrickscfg file at `token=`, reconnect databricks vscode extension if needed.

8. Install `databricks-connect` in current python environment, by running `pip install databricks-connect`.
9. In [test_notebook](./test_notebook.ipynb), it will be good to run cell 1 and make connection to databricks serverless compute.