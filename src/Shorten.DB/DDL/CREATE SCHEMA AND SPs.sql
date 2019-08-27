
CREATE TABLE ShortUrl
(
ShortUrlId int primary key identity (1,1) not null,
Code varchar(6) COLLATE Latin1_General_CS_AS unique not null,
OriginalUrl nvarchar(2083) not null,
CreatedAt Datetime not null,
LastUsage Datetime,
UsageCount int
)

GO

CREATE PROCEDURE uspGetShortUrl
(
@Code varchar(7)
)
AS

BEGIN

Select ShortUrlId, Code, OriginalUrl, CreatedAt, LastUsage, UsageCount
FROM ShortUrl
where Code  = @Code

END

GO


CREATE PROCEDURE uspInsertShortUrl
(
@Code varchar(6),
@OriginalUrl nvarchar(2083)
)
AS
BEGIN

Insert into ShortUrl (Code, OriginalUrl, CreatedAt, UsageCount) values (@Code, @OriginalUrl, GETUTCDATE(), 0)

END

GO


CREATE PROCEDURE uspUpdateUsage
(
@ShortUrlId int
)
AS

BEGIN

Update ShortUrl set LastUsage = GETUTCDATE(), UsageCount = UsageCount + 1
where ShortUrlId = @ShortUrlId

END







