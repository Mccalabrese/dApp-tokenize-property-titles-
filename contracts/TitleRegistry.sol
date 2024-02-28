pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract TitleRegistry is ERC721Full {
    constructor() public ERC721Full("TitleRegistryToken", "TIT") {}

    struct Title {
        string propertyOwner;
        string Jurisdiction;
        uint256 saleValue;
        string titleJson;
    }

    mapping(uint256 => Title) public savedTitles;

    event Sale(uint256 tokenId, uint256 saleValue, string reportURI, string titleJson);
    
    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return savedTitles[tokenId].titleJson;
    }


    function registerTitle(
        address owner,
        string memory name,
        string memory Jurisdiction,
        uint256 initialSaleValue,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        savedTitles[tokenId] = Title(name, Jurisdiction, initialSaleValue, tokenJSON);

        return tokenId;
    }

    function newSale(
        uint256 tokenId,
        uint256 newSaleValue,
        string memory reportURI,
        string memory tokenJSON
        
    ) public returns (uint256) {
        savedTitles[tokenId].saleValue = newSaleValue;

        emit Sale(tokenId, newSaleValue, reportURI, tokenJSON);

        return (savedTitles[tokenId].saleValue);
    }
}
