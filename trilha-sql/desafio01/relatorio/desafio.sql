with total_emails_enviados AS (
	SELECT 
	from_user,
	COUNT (*) as total_enviados
	FROM google_gmail_emails_extended
	GROUP BY from_user
)

SELECT from_user as Remetente,
total_enviados as Soma_de_emails_enviados,
RANK() OVER (ORDER BY total_enviados DESC) AS ranking,
DENSE_RANK() OVER (ORDER BY total_enviados DESC) AS dense_ranking,
ROW_NUMBER() OVER (ORDER BY total_enviados DESC, from_user ASC) AS row_num
FROM total_emails_enviados