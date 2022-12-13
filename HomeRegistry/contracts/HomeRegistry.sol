pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract HomeRegistry is ERC721Full {
    constructor() public ERC721Full("RealStateRegistryToken", "Home") {}

    struct Home {
        string home_address;
        string sqt_ft;
        string bedrooms;
        string bathrooms;
        uint256 home_value;
        string zillow_link;
        string yearbuilt;
    }

    mapping(uint256 => Home) public homeCollection;

    event Appraisal(uint256 tokenId, uint256 home_value, string reportURI);

    function registerhome(
        address owner,
        string memory home_address,
        string memory sqt_ft,
        string memory bedrooms,
        string memory bathrooms,
        uint256 home_value,
        string memory zillow_link,
        string memory yearbuilt,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        homeCollection[tokenId] = Home(home_address, sqt_ft, bedrooms, bathrooms, home_value, zillow_link, yearbuilt);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        homeCollection[tokenId].home_value = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return homeCollection[tokenId].home_value;
    }
}